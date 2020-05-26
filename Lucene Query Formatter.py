import sublime
import sublime_plugin


class LuceneQueryFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			for region in self.view.sel():
				selection=None
				# retrieve selected text and if nothing is selected, everything is retrieved
				if region.empty():
					selection=sublime.Region(0, self.view.size())
				else:
					selection=region
				s=self.view.substr(selection)
				if not s:
					sublime.message_dialog("Please provide some input text")
				else:
					print("Indenting Lucene Query...")
					sublime.status_message("Indenting Lucene Query...")
					#format query
					result=format(s)
					if result!=s:
						self.view.replace(edit, selection, result)
					print("Indented successfully")
					sublime.status_message("Indented successfully")	
		except Exception as error:
			sublime.message_dialog("Some internal error occured.\nQuery could not be processed. Please review the console for error.")
			print("Error occurred:")
			print(error)

#this method is used to format the query
def format(query):
	#remove white spaces
	query=removeSpaces(query)
	#remove "" around the query
	if query[0]=='\"' and query[-1]=='\"' and len(query)>=2:
		query=query[1:-1]
	result=""
	countTabs=0
	#inPhrase indicates whether we are traversing the quoted text
	inPhrase=False
	for idx in range(len(query)):
		if query[idx]=='\"':
			#toggle inPhrase when ' " ' is encountered
			inPhrase=1^inPhrase
			#jump onto the next line after completing each phrase(quoted text)
			result=result+query[idx]
			if inPhrase==False:
				result=result+"\n"
				result=result+("\t"*countTabs)
			continue
		#quoted text should be printed as it is
		if inPhrase==True:
			result=result+query[idx]
			#in case quoted text contains newline character, cursor should move onto the next line but should not change the current block
			if query[idx]=='\n':
				result=result+("\t"*countTabs)
			continue
		#remove exisiting spacing characters from the string
		if query[idx]==' ' or query[idx]=='\t' or query[idx]=='\n' or query[idx]=='\r':
			continue
		#handle ',' separately
		if query[idx]==',':
			#incase cursor is at the starting of a new line, add tab spacing to get into the current block
			if result[-1]=='\n':
				result=result+("\t"*countTabs)
			#append ','
			result=result+query[idx]
			#jump onto new line and respective indent block after each ','
			result=result+"\n"
			result=result+("\t"*countTabs)
		#start a new block whenever an opening paranthesis is encountered
		elif query[idx]=='(' or query[idx]=='[' or query[idx]=='{':
			result=result+query[idx]
			#jump onto the next line and add a new block by increasing number of tabs
			result=result+"\n"
			countTabs=countTabs+1
			result=result+("\t"*countTabs)
		#end the current block whenever a closing paranthesis is encountered
		elif query[idx]==')' or query[idx]==']' or query[idx]=='}':
			#if the cursor has already moved onto the next line, remove '\t' from end as cursor needs to go back to the previous block
			if result[-1]=='\t':
				result=result[:-1]
			#otherwise, move onto the next line, get onto the previous block
			else:
				result=result+"\n"
				result=result+("\t"*(countTabs-1))
			#decrement tabCount due to closing of the block
			countTabs=countTabs-1
			result=result+query[idx]
			#incase there is a ',' after closing a block, it has to be printed just after closing so continue without moving onto the next line
			if idx<(len(query)-1) and query[idx+1]==',':
				continue
			#otherwise, move onto the next line, jump onto the current block
			result=result+"\n"
			result=result+("\t"*countTabs)
		#in any other cases, just print the character
		else:
			result=result+query[idx]	
	return result

#this function is used to remove blanks around the query
def removeSpaces(query):
	l=0
	r=len(query)-1
	while l<len(query) and (query[l]==' ' or query[l]=='\r' or query[l]=='\t' or query[l]=='\n'):
		l=l+1;
	while r>=0 and (query[r]==' ' or query[r]=='\r' or query[r]=='\t' or query[r]=='\n'):
		r=r-1
	if l>r:
		return ""
	return query[l:r+1]