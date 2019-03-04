args = commandArgs(trailingOnly=TRUE)

files = list.files(args[1], '.csv$', full.names=TRUE)
for (path in files) {
    print(path)
    filename = unlist(strsplit(path, '[.]'))[1]

    data = read.csv(path, header=TRUE)
    png(paste(filename, '.png', sep=''), width = 1280, height = 768)
    temp_par = par()
    par(mar = c(6, 5, 5, 4)+0.1)

    # Wav
    x = as.matrix(data['time'][data['flag']=='wav'])
    y = as.matrix(data['point'][data['flag']=='wav'])
    plot(x, y, 
         type='l',
         xlim=c(0, round(max(data['time']))+1),
         ylim=c(-0.5, round(max(data['point']))+0.5),
         main=unlist(strsplit(filename, '[/]'))[length(unlist(strsplit(filename, '[/]')))],
         xlab='Time (seconds)', ylab=NA,
         yaxt='n',
         cex.main=1.5, cex.lab=1.5, cex.axis=1.5)

    # Data
    x = as.matrix(data['time'][data['flag']=='up'])
    y = as.matrix(data['point'][data['flag']=='up'])
    lines(x, y, type='p', pch=24, col='blue', cex=3)
    x = as.matrix(data['time'][data['flag']=='down'])
    y = as.matrix(data['point'][data['flag']=='down'])
    lines(x, y, type='p', pch=25, col='red', cex=3)

#    for (pivot in seq(1, round(max(data['point'])))) {
#        x = as.matrix(data['time'][
#                (data['flag']=='up'|data['flag']=='down') &
#                round(data['point'])==pivot])
#        y = as.matrix(data['point'][
#                (data['flag']=='up'|data['flag']=='down') &
#                round(data['point'])==pivot])
#        lines(x, y, type='p', 
#              pch=ifelse(y%%1<0.5, 24, 25),
#              col=ifelse(y%%1<0.5, 'blue', 'red'),
#              cex=3)
#    }
    # TCP Flags
    x = as.matrix(data['time'][data['flag']=='syn'])
    y = as.matrix(data['point'][data['flag']=='syn'])
    lines(x, y, type='p', pch=9, col='green', cex=4)
    x = as.matrix(data['time'][data['flag']=='fin'])
    y = as.matrix(data['point'][data['flag']=='fin'])
    lines(x, y, type='p', pch=9, col='yellow', cex=4)
    x = as.matrix(data['time'][data['flag']=='ssl'])
    y = as.matrix(data['point'][data['flag']=='ssl'])
    lines(x, y, type='p', pch=9, col='brown', cex=4)
    # DNS
    x = as.matrix(data['time'][data['flag']=='dns'])
    y = as.matrix(data['point'][data['flag']=='dns'])
    lines(x, y, type='p', pch=13, col='black', cex=4)

    # background
    for (pivot in seq(1, round(max(data['point'])))) {
        abline(h=pivot, lty=2, col='brown', lwd=2)
        if (pivot%%2 != 0) {
            rect(0-1, pivot-0.5, round(max(data['time']))+1+1, pivot+0.5, 
                 col=rgb(0, 0, 0, alpha=0.1),
                 border=FALSE)
        }
    }

    # header
    par(xpd = TRUE)
    head_file = paste(filename, '.head', sep='')
    head_data = read.csv(head_file, header=FALSE, sep=",")
    for (index in seq(1, round(max(data['point'])))) {
        text(x=0, y=index, 
             labels=ifelse(is.na(as.character(head_data[['V2']][index])) | as.character(head_data[['V2']][index])=='',
                           as.character(head_data[['V1']][index]),
                           as.character(head_data[['V2']][index])),
             cex=1.25)
    }

    # abline
    line_file = paste(filename, '.line', sep='')
    line_data = read.csv(line_file, header=FALSE, sep=',')
    labels = c('callStart', 'callEnd',
               'commandStart', 'commandEnd',
               'actionStart', 'actionEnd')
    for (index in seq(1, 6)) {
        abline(v=line_data['V1'][index,], lty=2, col='black')
        text(line_data['V1'][index,], ifelse(index%%2==1, -0.5, -0.55), labels[index], cex=1.25)
    }

    # legend
    legend('bottomright',
           legend=c('Data Upload', 'Data Download', 'TCP SYN', 'TCP FIN', 'SSL Handshake',
                    'DNS'),
           col=c('blue', 'red', 'green', 'yellow', 'brown', 'black'),
           pch=c(24, 25, 9, 9, 9, 13))

    par = temp_par
    dev.off()
}
