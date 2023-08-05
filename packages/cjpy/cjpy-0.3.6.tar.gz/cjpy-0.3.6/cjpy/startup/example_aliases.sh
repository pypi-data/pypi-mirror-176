
export CJSON_STARTDIR=~/rlocal/jpy/startup
export CJSON_STARTUP=$CJSON_STARTDIR/startup.json5
export CJSON_PIP=cjpy.

alias cjpy='python3 -m cjpy'

alias      peval='cjpy --^parse --main eval -*-pars x --show output -x'
alias        pow='cjpy --^parse --main pow -*-pars x,y --show output'

alias     rename='cjpy --^parse --main ${CJSON_PIP}cmdscript.rename --load $CJSON_STARTDIR/${CJSON_PIP}cmdline.json5 -clobber --timekey infile --sizekey infile -infile'
alias     search='cjpy --^parse --main ${CJSON_PIP}cmdscript.search --load $CJSON_STARTDIR/${CJSON_PIP}cmdline.json5 -infile'

alias   csv2fits='cjpy --^parse --main ${CJSON_PIP}tabletool.csv2fits -ftype csv  -indir . -infile'
alias   csv2list='cjpy --^parse --main ${CJSON_PIP}tabletool.list -ftype csv -infile'
alias     filter='cjpy --^parse --main ${CJSON_PIP}tabletool.filter   -indir . -infile'
alias filterfits='cjpy --^parse --main ${CJSON_PIP}tabletool.filter   -ftype fits --keymap:sort _sort -indir . -infile'
alias   fits2csv='cjpy --^parse --main ${CJSON_PIP}tabletool.csv2fits -ftype fits -indir . -infile'
alias  fits2list='cjpy --^parse --main ${CJSON_PIP}tabletool.list -ftype fits -infile'
alias   tab2list='cjpy --^parse --main ${CJSON_PIP}tabletool.list -infile'
alias   readfits='cjpy --^parse --main ${CJSON_PIP}tabletool.readfits -indir . -infile'
alias     lsfits='cjpy --^parse --main ${CJSON_PIP}tabletool.lsfits   --load $CJSON_STARTDIR/cmdline.json5 -indir . -infile'

alias   mollview='cjpy --^parse --main ${CJSON_PIP}plottool.hp2mollview -infile'
alias     plot1d='cjpy --^parse --main ${CJSON_PIP}plottool.plot1d  --load $CJSON_STARTDIR/${CJSON_PIP}cmdline.json5 -infile'
alias      dplot='cjpy --^parse --main ${CJSON_PIP}plottool.dplot   --load $CJSON_STARTDIR/${CJSON_PIP}cmdline.json5 -infile'
alias    plotdmr='cjpy --^parse --main ${CJSON_PIP}plottool.plotDMR --load $CJSON_STARTDIR/${CJSON_PIP}cmdline.json5 -infile'
alias    mplot1d='cjpy --^parse --load $CJSON_STARTDIR/${CJSON_PIP}mplot1d.json5 -infile'
alias   scplot1d='cjpy --^parse --load $CJSON_STARTDIR/${CJSON_PIP}scan_cols_plot1d.json5 -infile'
alias   shplot1d='cjpy --^parse --load $CJSON_STARTDIR/${CJSON_PIP}scan_hdus_plot1d.json5 -infile'
