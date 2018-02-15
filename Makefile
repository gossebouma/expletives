
TREEBANKDIR = ud-treebanks-v2.1
stats :
	for i in `ls -d $(TREEBANKDIR)/* | cut -f2 -d'/' ` ; \
	   do ( make $$i.stats ;  make $$i.sum ; make $$i.freq ; make $$i.patterns ) done
	find . -name '*.stats' -size 0 | xargs rm
	find . -name '*.patterns' -size 0 | xargs rm
	grep -l '^0$' *.sum | xargs rm
	grep -l '^0.00000$' *.freq | xargs rm

%.stats :
	grep -hw expl $(TREEBANKDIR)/$*/*.conllu \
  | cut -f2,3,4,8 | tr 'A-Z' 'a-z' | sort | uniq -c > $@
%.sum :
	cat $(TREEBANKDIR)/$*/*.conllu | grep -cw expl > $@
%.wc :
	cat  $(TREEBANKDIR)/$*/*.conllu | grep -c '^[0-9]' > $@

%.freq : %.wc %.sum 
	paste $*.sum $*.wc |xargs perl -e 'printf("%.5f\n", $$ARGV[0]/$$ARGV[1])' > $@

%.patterns :
	cat $(TREEBANKDIR)/$*/*.conllu | ./expletive_usage.py3 > $@
