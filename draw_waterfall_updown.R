args = commandArgs(trailingOnly=TRUE)

files = list.files(args[1], '.csv$', full.names=TRUE)
for (path in files) {
    print(path)
    filename = unlist(strsplit(path, '[.]'))[1]

    data = read.csv(path, header=TRUE)
    png(paste(filename, '.png', sep=''), width = 1280, height = 768)
    temp_par = par()
    par(mar = c(6, 5, 5, 4)+0.1)

    x = as.matrix(data['time'][round(data['point'])==0])
    y = as.matrix(data['point'][round(data['point'])==0])
    plot(x, y, 
         type='l',
         xlim=c(0, round(max(data['time']))+1),
         ylim=c(-0.5, round(max(data['point']))+0.5),
         main=filename,
         xlab='Time (seconds)', ylab=NA,
         yaxt='n',
         cex.main=1.5, cex.lab=1.5, cex.axis=1.5)

    for (pivot in seq(1, round(max(data['point'])))) {
        x = as.matrix(data['time'][round(data['point'])==pivot])
        y = as.matrix(data['point'][round(data['point'])==pivot])
        lines(x, y, type='p', 
              pch=ifelse(y%%1<0.5, 24, 25),
              col=ifelse(y%%1<0.5, 'blue', 'red'),
              cex=3)
        abline(h=pivot, lty=2, col='brown', lwd=2)
        if (pivot%%2 != 0) {
            rect(0-1, pivot-0.5, round(max(data['time']))+1+1, pivot+0.5, 
                 col=rgb(0, 0, 0, alpha=0.1),
                 border=FALSE)
        }
    }

    par(xpd = TRUE)
    head_file = paste(filename, '.head', sep='')
    head_data = read.csv(head_file, header=FALSE, sep=",")
    for (index in seq(1, round(max(data['point'])))) {
        text(0, index, head_data['V1'][index,], cex=1.25)
    }


    line_file = paste(filename, '.line', sep='')
    line_data = read.csv(line_file, header=FALSE, sep=',')
    labels = c('callStart', 'callEnd',
               'commandStart', 'commandEnd',
               'actionStart', 'actionEnd')
    for (index in seq(1, 6)) {
        abline(v=line_data['V1'][index,], lty=2, col='black')
        text(line_data['V1'][index,], ifelse(index%%2==1, -0.5, -0.55), labels[index], cex=1.25)
    }

    par = temp_par
    dev.off()
}
