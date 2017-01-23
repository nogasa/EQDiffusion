#!/usr/bin/env Rscript --no-save

###
#	test_fit.R
#	/Users/abarbour/survey.processing/local.projects/EQDiffusion/data/forandy
#	Created by 
#		/Users/abarbour/bin/ropen ( v. 2.6.2 )
#	on 
#		2017:019 (19-January)
###

## local functions
#try(source('funcs.R'))

## libs

#if (!require("pacman")) install.packages("pacman", dependencies=TRUE)
#pacman::p_load(package1, package2, package_n)

# loads core tidy packages:  ggplot2, tibble, tidyr, readr, purrr, and dplyr
library(tidyverse)
#tidyverse_conflicts()
#tidyverse_update(TRUE)

## local/github libs
# devtools::install_github("abarbour/kook")
#library(kook)
#Set1 <- brew.set1()
#Set1l <- brew.set1(TRUE)
#Dark2 <- brew.dark2()
#Dark2l <- brew.dark2(TRUE)
#Dark2ll <- brew.dark2(TRUE,TRUE)

#+++++++++++

shake <- FALSE
redo <- FALSE

readr::read_table("xyz_34", col_names=c("yr","mo","dy","hr","mi","sec","Mw","lat","lon","depth","ndist","reftime.hr")) %>%
	dplyr::mutate(
		reftime.s = reftime.hr * 3600,
		ddist = sqrt(4*pi*diffusiv*(reftime.s - reftime.s[1])), 
		ndist.diff = ddist/max(ddist)) -> b34


read.table('burstinfo', header=TRUE) -> bursts

subset(bursts, bid==34) -> b34meta
stopifnot(nrow(b34meta)==1)
diffusiv <- b34meta$D

#+++++++++++

plot(ndist ~ reftime.hr, b34)
lines(ndist.diff ~ reftime.hr, b34)

sqrt(coef(lm(ndist*sqrt(4 * pi *diffusiv * reftime.s) ~ sqrt(reftime.s), b34))/2/pi)

#+++++++++++

#FIG <- function(x, ...){
#}

#if (shake){
#    FIG() 
#} else {
#    figfi <- "some_figure"
#    h <- 7
#    w <- 7
#    niceEPS(figfi, h=h, w=w, toPDF=TRUE)
#    try(FIG())
#    niceEPS()
#    nicePNG(figfi, h=h, w=w)
#    try(FIG())
#    nicePNG()
#}

###
#kook::warn_shake()
