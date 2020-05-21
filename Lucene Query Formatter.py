import sublime
import sublime_plugin


class LuceneQueryFormatterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			for region in self.view.sel():
				selection=None
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
					result=format(s)
					if result!=s:
						self.view.replace(edit, selection, result)
					print("Indented successfully")
					sublime.status_message("Indented successfully")	
		except Exception as error:
			sublime.message_dialog("Some internal error occured.\nQuery could not be processed. Please review the console for error.")
			print("Error occurred:")
			print(error)

def format(query):
	query=removeSpaces(query)
	if query[0]=='\"' and query[-1]=='\"' and len(query)>=2:
		query=query[1:-1]
	result=""
	countTabs=0
	inPhrase=False
	for idx in range(len(query)):
		if query[idx]=='\"':
			inPhrase=1^inPhrase
			result=result+query[idx]
			if inPhrase==False:
				result=result+"\n"
				for i in range(countTabs):
					result=result+"\t"
			continue
		if inPhrase==True:
			result=result+query[idx]
			if query[idx]=='\n':
				for i in range(countTabs):
					result=result+"\t"
			continue
		if query[idx]==' ' or query[idx]=='\t' or query[idx]=='\n' or query[idx]=='\r':
			continue
		if query[idx]==',':
			if result[-1]=='\n':
				for i in range(countTabs):
					result=result+"\t"
			result=result+query[idx]
			result=result+"\n"
			for i in range(countTabs):
				result=result+"\t"
		elif query[idx]=='(' or query[idx]=='[' or query[idx]=='{':
			result=result+query[idx]
			result=result+"\n"
			countTabs=countTabs+1
			for i in range(countTabs):
				result=result+"\t"
		elif query[idx]==')' or query[idx]==']' or query[idx]=='}':
			if result[-1]=='\t':
				result=result[:-1]
			else:
				result=result+"\n"
				for i in range(countTabs-1):
					result=result+"\t"
			countTabs=countTabs-1
			result=result+query[idx]
			if idx<(len(query)-1) and query[idx+1]==',':
				continue
			result=result+"\n"
			for i in range(countTabs):
				result=result+"\t"
		else:
			result=result+query[idx]	
	return result

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