# invoiceManangement
Django-rest-apis to upload a pdf file and extract structured invoice information and perform updates on invoices
invoice management contains APIs for the following:
- To allow a customer to provide a PDF document (invoice) to process
				The file is uploaded and invoice gets generated
			- To allow a customer to track a document’s digitization status
				-APIs to view file along with structured invoice information are provided
			- To allow a customer to retrieve the structured invoice information for a specified document, if the document status is digitized 
				-APIs to view invoice information given filename as input
			-To allow a staff member (or another microservice) to manually add digitized / parsed (​structured​) information for a specific document 
				-APIs to manually update any piece of information without requiring all fields to be updated
			-To add/update more than one field at a time, if the caller chooses to do so
				-API to add or updated items in an invoice given the filename and items as input
			-To allow marking a document as “digitized” 
				-APIs to allow marking a document as digitized
