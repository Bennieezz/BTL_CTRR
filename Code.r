
library(igraph)
  # Function to read graph data from TSV file
  #setwd(E:\BTL_CTRR)
  read_graph_from_tsv <- function(file_path) {
       edges <- read.table(file_path, header = FALSE, col.names = c("from", "to", "weight"))
       graph <- graph_from_data_frame(edges, directed = FALSE)
       return(graph)
    }
  
     # File path to your TSV file
     file_path <- "E:/BTL_CTRR/roadNet-CA_adj.tsv"

     
       # Read graph from TSV file
       my_graph <- read_graph_from_tsv(file_path)
       
         # Plot the graph or perform any other operations
         plot(my_graph, vertex.label.dist = 2, layout = layout_with_fr)
         
         