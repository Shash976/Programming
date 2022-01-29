from django.shortcuts import render
from . import util
import re

# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content=util.get_entry(title)
    if content != None:
        return render(request, "encyclopedia/entry.html", {"content":content, "title": title.upper()})
    return render(request, "encyclopedia/error.html")

def search(request):
    total_entries=util.list_entries()
    query = request.GET.get('q')
    results=[]
    for entry in total_entries:
        if re.search(query, entry, re.IGNORECASE):
            results.append(entry)
            rg=f"^{query}$"
            raw= r'{}'.format(rg)
            if re.search(raw, entry, re.IGNORECASE):
                content=util.get_entry(entry)
                return render(request, "encyclopedia/entry.html", {"content":content, "title": entry.upper()})
    return render(request, "encyclopedia/search.html", {"results":results, "query":query, "res":len(results)!=0})

def new_page(request):
    return render(request, "encyclopedia/create.html")