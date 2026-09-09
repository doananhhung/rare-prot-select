RhpcBLASctl::blas_set_num_threads(1)
RhpcBLASctl::omp_set_num_threads(1)

Sys.setenv(OMP_NUM_THREADS = 1, OPENBLAS_NUM_THREADS = 1, MKL_NUM_THREADS = 1, VECLIB_MAXIMUM_THREADS = 1, NUMEXPR_NUM_THREADS = 1)
library(readxl)
library(tidyverse)
library(reticulate)
library(seqinr)

calculateGains <- function(set, sim_matrix) {
  if (length(set) == 0) {
    return(0)
  }
  df <- as.matrix(sim_matrix[set, ]) %>% t()
  return(sum(matrixStats::rowMaxs(df)) )
}

facilityLocationBiGreedy <- function(identMat_tmp, IDsNames) {

  IDsNum <- c(1:length(IDsNames))

  setToGrow <- c()
  setToShrink <- IDsNum


  for (i in IDsNum) {
    alphaS <- c(setToGrow, i)
    betaS <- setToShrink[!(setToShrink == i)]

    alpha_i <- calculateGains(alphaS, identMat_tmp) - calculateGains(setToGrow, identMat_tmp)
    beta_i <- calculateGains(betaS, identMat_tmp) - calculateGains(setToShrink, identMat_tmp)
    if (beta_i == 0) {
      beta_i <- calculateGains(setToShrink, identMat_tmp)
    }
    # alpha_i >= abs(beta_i)

    if (alpha_i/sum(alpha_i + beta_i) > 0.5) {
      setToGrow <- c(setToGrow, i)
      setToShrink <- setToShrink
    } else {
      setToGrow <- setToGrow
      setToShrink <- setToShrink[!(setToShrink == i)]
    }
  }

  # message(identical(setToGrow, setToShrink))

  return(IDsNames[setToGrow])
}




use_condaenv("r4-base")

famDataPath <- "/data/han/projects/ThYme/data-all/"
famC <- "TE"
dbPath <- paste0(famDataPath, famC, "_db")

famDF <- read_excel(paste0(famDataPath, famC, ".xlsx")) %>%
   dplyr::select(Family, Organism, `Protein name`) %>%
  drop_na()
famCCount <- as.data.frame(table(famDF$Family)) %>%
   `colnames<-`(c("Family", "Count"))

famFasta <- read.fasta(file = paste0(famDataPath, famC, ".fasta"))

allFamNames <- data.frame(
  seqID = lapply(famFasta, function(s) {
    attributes(s)$name
  }) %>% unlist(),
  family = famDF$Family,
  stringsAsFactors = FALSE
)

allRes <- NULL
allReport <- NULL
for (i in 1:nrow(famCCount)) {
  fam <- famCCount[i, 'Family']
  n <- famCCount[i, 'Count']
  message("Family: ", fam)

  if (n <= 2) {
    next
  }

  idx <- which(famDF$Family == fam)
  famToWork <- famFasta[idx]
  names(famToWork) <- NULL

  famSq <- lapply(famToWork, function(s) {
    paste0(toupper(s), collapse = "")
  })
  namesSq <- lapply(famToWork, function(s) {
    attributes(s)$name
  }) %>% unlist()

  annotSq <- lapply(famToWork, function(s) {
    attributes(s)$Annot
  }) %>% unlist()
  fastaf <- paste0("/data/han/projects/ThYme/tmp/", fam, ".fasta")
  simf <- paste0("/data/han/projects/ThYme/tmp/", fam, ".txt")
  write.fasta(famSq, names = gsub(">", "",annotSq), file.out = fastaf)

  command_line <- paste0("blastp -query ", fastaf, " -subject ", fastaf,
                         " -evalue 0.05 -max_target_seqs 100 -word_size 3 -outfmt ",
                         "'6 qseqid sseqid pident'",
                         " -out ", simf
  )

  system(command_line)

  identDat <- read.table(simf)
  colnames(identDat) <- c("queryID", "sourceID", "perc_ident")
  identDat$perc_ident <- identDat$perc_ident/100
  identDat <- identDat[order(-identDat$perc_ident),]
  checkDup <- paste0(identDat$queryID, "___", identDat$sourceID)
  identDat <- identDat[!duplicated(checkDup),]

  identMat <- spread(identDat, sourceID, perc_ident)
  allIDs <- as.character(identMat$queryID)
  identMat <- identMat[,-1]
  rownames(identMat) <- allIDs

  # allRes_Greedy <- allRes_BiGreedy <- c()
  allRes_BiGreedy  <- c()
  j <- 1
  while (j < 1001) {

    IDsNames <- sample(allIDs)
    identMat_tmp <- as.matrix(identMat[IDsNames,IDsNames])
    # identMat_tmp <- identMat
    # IDsNames <- rownames(identMat_tmp)
    # IDsNames <- allIDs_shuffle
    identMat_tmp <- as.matrix(identMat_tmp)
    identMat_tmp[is.na(identMat_tmp)] <- 0
    rownames(identMat_tmp) <- colnames(identMat_tmp) <- NULL

    # res_Greedy <- facilityLocationGreedy(identMat_tmp, IDsNames, threshold = 0.9)
    res_BiGreedy <- facilityLocationBiGreedy(identMat_tmp, IDsNames)

    # allRes_Greedy <- c(allRes_Greedy, res_Greedy)
    allRes_BiGreedy <- c(allRes_BiGreedy, res_BiGreedy)
    j <- j + 1

  }

  df <- as.data.frame(table(allRes_BiGreedy))
  colnames(df) <- c("repID", "count")
  df <- df[order(-df$count),]
  # df$Family <- rep(fam, nrow(df))
  countV <- df$count
  names(countV) <- as.character(df$repID)
  # df2 <- as.data.frame(table(allRes_BiGreedy))
  candidateS <- names(countV)[countV == max(countV)]
  commonS <- length(candidateS)
  fastadbf <- paste0("/data/han/projects/ThYme/data-db/", fam, ".fasta")

  while(commonS <= nrow(df)) {
    candidateIDX <- which(namesSq %in% candidateS)
    write.fasta(famSq[candidateIDX], names = gsub(">", "",annotSq[candidateIDX]), file.out = fastadbf)
    query_cli <- paste0("blastp -query ", fastadbf, " -db ", dbPath,
                        " -max_target_seqs 999999 -evalue 1e-7 -num_threads 4 -outfmt ",
                        "'6 qseqid sseqid pident'",
                        " -out /data/han/projects/ThYme/data-db/", fam, ".txt"
    )

    system(query_cli)

    tmp <- read.table(paste0("/data/han/projects/ThYme/data-db/", fam, ".txt"))
    idS <- unique(tmp[,2])

    idGT <- allFamNames$seqID[allFamNames$family == fam]
    idGT_n <- allFamNames$seqID[!(allFamNames$family == fam)]

    tmpReport <- data.frame(
      family = fam,
      alogrithm = "bigreedy",
      num_Rep = length(candidateS),
      sensitivity = length(intersect(idS, idGT))/ length(idGT),
      specificity = 1 - length(intersect(idS, idGT_n))/ length(idGT_n),
      stringsAsFactors = FALSE
    )

    allReport <- rbind(allReport, tmpReport)


    tmpC <- length(intersect(unique(tmp[,2]), namesSq))
    if (tmpC >= length(namesSq)) {
      commonS <- nrow(df) + 2
    } else {
      commonS <- commonS + 1
      candidateS <- c(candidateS, names(countV)[commonS])
    }
  }

  candidateSave <- paste0("/data/han/projects/ThYme/res-bigreedy/", fam, ".fasta")
  candidateIDX <- which(namesSq %in% candidateS)
  write.fasta(famSq[candidateIDX], names = gsub(">", "",annotSq[candidateIDX]), file.out = candidateSave)


  tmpdf <- data.frame(seqID = unique(tmp[,2]),
                      family = rep(fam, length(unique(tmp[,2]))),
                      stringsAsFactors = FALSE
                      )
  allRes <- rbind(allRes, tmpdf)
}

saveRDS(allRes, "/data/han/projects/ThYme/allRes-bigreedy.rds")
saveRDS(allReport, "/data/han/projects/ThYme/allReport-bigreedy.rds")


allResFam <- unique(allRes$family)
allFamNames <- data.frame(
  seqID = lapply(famFasta, function(s) {
    attributes(s)$name
  }) %>% unlist(),
  family = famDF$Family,
  stringsAsFactors = FALSE
)
rownames(allFamNames) <- NULL
reportDF <- NULL
for (fam in allResFam) {
  idS <- allRes$seqID[allRes$family == fam]
  idGT <- allFamNames$seqID[allFamNames$family == fam]
  idGT_n <- allFamNames$seqID[!(allFamNames$family == fam)]
  repdf <- data.frame(
    family = fam,
    sensitivity = length(intersect(idS, idGT))/ length(idGT),
    specificity = 1 - length(intersect(idS, idGT_n))/ length(idGT_n),
    stringsAsFactors = FALSE
  )
  reportDF <- rbind(reportDF, repdf)


}