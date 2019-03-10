args = commandArgs(trailingOnly=TRUE)

files = list.files(args[1], '.csv$', full.names=TRUE)
for (path in files) {
    print(path)
    data = read.csv(path, header=TRUE)
    
    filename = unlist(strsplit(path, "[.]"))[1]
    png(paste(filename, '.png', sep=''), width = 1280, height = length(as.matrix(data[1]))*25+200)
    temp_par = par()
    par(mar = c(6, 5, 5, 4)+0.1)
    par(xpd = TRUE)
    padding = data[[3]][1]
    barplot(t(as.matrix(data[11]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkgoldenrod1'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            xlab='Load time (s)',
            cex.main=1.5)
    barplot(t(as.matrix(data[15]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkslategray4'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[14]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkslategray2'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[13]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('goldenrod4'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[12]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkgoldenrod1'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[10]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[9]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('gray'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[8]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[7])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkred'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[6])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[5])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkseagreen4'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[4])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[3])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('darkseagreen1'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[2])),
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)
    barplot(t(as.matrix(data[16]))+padding,
            horiz=TRUE,
            names.arg=as.matrix(data[1]),
            col=c('white'),
            border=NA,
            yaxt='n',
            xlim=c(0, ceiling(max(data[2:15])/5)*5),
            cex.main=1.5,
            add=TRUE)

    labs = as.matrix(data[1])
    text(x=1,
         y=seq(1, length(as.matrix(data[1])))*1-0.05,
         labs)

    legend(x="topright", inset = 0.015,
           legend=c('Call', 'Command', 'Action', 
                    'DNS', 'Connect', 'SecureConnect',
                    'Request', 'Response'),
           fill =c('darkseagreen1', 'darkseagreen4', 'darkred',
                   'gray', 'darkgoldenrod1', 'goldenrod4', 
                   'darkslategray2', 'darkslategray4'))

    par = temp_par
    dev.off()
}
