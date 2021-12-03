#remotes::install_github("Zoological-Society-of-London/rlpi", dependencies=TRUE)
library(janitor)
library(dplyr)
library(rlpi)
library(tidyr)

df <- clean_names(read.csv("data/LPD - LPR2020data_public.csv"))

df$clean_units[df$clean_units == ""] <- NA

df_long <- df %>% 
  dplyr::select(id,binomial, country,common_name, units,clean_units,starts_with("X")) %>% 
  pivot_longer(starts_with("x")) %>% 
  mutate(merge_units = coalesce(clean_units, units)) %>% 
  mutate(year = as.numeric(gsub("x","", name))) %>% 
  select(Binomial = binomial,ID = id,year,popvalue = value)

df_long$popvalue[df_long$popvalue == "NULL"] <- NA
df_long$popvalue <- as.numeric(df_long$popvalue)

df_long <- df_long %>% filter(!is.na(popvalue))


ug <- df %>% 
  filter(region == "Latin America and Caribbean") %>% 
  select(binomial) %>% 
  pull()

sp_binom = c("Panthera_leo")

make_files <- function(sp_binom, sel_name = "test"){
  
  sp_sel <- df_long %>% 
    filter(Binomial %in% sp_binom)
  
  pop_file = paste0("data/",sel_name, "_pops.txt")
  write.table(sp_sel, pop_file, row.names=FALSE,sep="\t", quote = FALSE)
  
  infile = data.frame("FileName" = pop_file, "Group" = 1, "Weighting" = 1)
  infile_name = paste0("data/",sel_name, "_infile.txt")
  write.table(infile, infile_name,row.names=FALSE,sep="\t", quote = FALSE)
  return(infile_name)
  
}


infile = make_files(sp_binom)

Nearc_lpi <- LPIMain(infile, use_weightings = 1, VERBOSE=FALSE)


ggplot(sp_sel, aes(x = year, y = popvalue, group = ID))+
  geom_line()+
  geom_point()+
  facet_wrap(.~ID, scales = "free_y")
