import csv
import json
from numpy import genfromtxt
import numpy as np

fout=open('pft_subject_info.csv', 'w')

workflows=np.array([16], dtype=np.int) # list the workflows you have 

i=long(0)

with open('./p4t_subjectsdump.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
                tmp=json.loads(row['metadata'])
		loc=json.loads(row['locations'])	 
                x=tmp.keys()
       
                subject_set_id= int(row['subject_set_id'])

		# only do this for the subject sets you're intersted in - basically skipping beta test data and anything you don't want to parse 
                if not ((subject_set_id == 373) or (subject_set_id == 249) or (subject_set_id == 32519) or (subject_set_id == 91451) or (subject_set_id == 12814) or (subject_set_id ==33)):
                        continue 

		
		# setup the header for the first row 
		if (i==0):
			fout.write('subject_id, workflow_ids, subject_set_id')


			for workflow in workflows:
				fout.write(", workflow_"+str(workflow)+'_classification_count,'+"retired in_workflow_"+str(workflow))
			fout.write( ',image_1_url')

			# printing the columns of the metadata uploaded from the manifest file at the time of subject upload 	
			for q in x:
				fout.write( ','+q)
			fout.write('\n')	


		# now parse the info for output 
		livepftid=row['subject_id']
		
		fout.write( livepftid+','+row['workflow_ids']+','+row['subject_set_id'])


			
		# parse the retired state 
		retired=row['retired_in_workflow']
		# remove the brackets
		retired=retired[1:len(retired)-1]
		retired = retired.split(",)")


		# for each workflow output as a separate column the classification count and the retired status of the subject 
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


		# outputing all the metadata inputted from the manifest file
		for q in x:
			fout.write(','+tmp[q])


		fout.write('\n')
		i=i+1

fout.close()		
