

var text = current.short_description + ' ' + current.description + ' ' + current.category;
var tagger = new global.AutoTagger();
tagger.addTags('incident', current.sys_id, current.number, text);


global.action.setRedirectURL(current);
