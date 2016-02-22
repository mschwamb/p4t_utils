import csv
import json
from numpy import genfromtxt
import numpy as np

fout=open('pft_subject_info.csv', 'w')

workflows=np.array([16], dtype=np.int)

i=long(0)

with open('./p4t_subjectsdump.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
                tmp=json.loads(row['metadata'])
		loc=json.loads(row['locations'])	 
                x=tmp.keys()
       
                subject_set_id= int(row['subject_set_id'])
                if not ((subject_set_id == 73) or (subject_set_id == 29049) or (subject_set_id == 2519) or (subject_set_id == 3451) or (subject_set_id == 2384) or (subject_set_id ==3339)):
                        continue 

		if (i==0):
			fout.write('subject_id, workflow_ids, subject_set_id')

			for workflow in workflows:
				fout.write(", workflow_"+str(workflow)+'_classification_count,'+"retired in_workflow_"+str(workflow))
			fout.write( ',image_1_url')
	
			for q in x:
				fout.write( ','+q)
			fout.write('\n')	

		livepftid=row['subject_id']
		
		fout.write( livepftid+','+row['workflow_ids']+','+row['subject_set_id'])


		retired=row['retired_in_workflow']
		# remove the brackets
		retired=retired[1:len(retired)-1]
		retired = retired.split(",)")

		classification_count=row['classifications_by_workflow']
		classification_count= json.loads(row['classifications_by_workflow'])	
		for workflow in workflows:
			fout.write(','+str( classification_count[str(workflow)]))


			found='False'

			for r in retired:	
				if (str(workflow) == r):
					found='True'
		
			fout.write(','+found)
		
		fout.write(','+str(loc['0']))

		for q in x:
			fout.write(','+tmp[q])


		fout.write('\n')
		i=i+1

fout.close()		
