
train_all :
	/bin/rm -rf /local/data/line/Projet_ENSG/Training_data/training_output
	cd  /local/data/line/Projet_ENSG/Projet_Recherche_ENSG ; (echo y ; echo y) | python3 train_all-in-one.py -v /local/data/line/Projet_ENSG/Training_data/raw_videos_input -s /local/data/line/Projet_ENSG/Training_data/srt_21.01.2020 -o /local/data/line/Projet_ENSG/Training_data/training_output 1> training_stdout.log.txt 2> training_stderr.log.txt
	ls -lR /local/data/line/Projet_ENSG/Training_data/training_output/ > training_output_ls-lR.log

sync :
	git push ; git commit -a -m 'from makefile' ; git push

