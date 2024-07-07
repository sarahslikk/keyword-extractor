var AutoTagger = Class.create();
AutoTagger.prototype = {
    initialize: function() {},

    addTags: function(tableName, recordId, recordNumber, text) {
        var tags = this._extractKeyWords(text);
        var addedTags = [];

        for (var i = 0; i < tags.length; i++) {
            var tagName = tags[i];
            var tagSysId = this._getOrCreateTag(tagName);

            if (tagSysId) {
                this._addTagToRecord(tagSysId, tableName, recordId, recordNumber);
                addedTags.push(tagName);
            }
        }

        gs.addInfoMessage('Tags added: ' + addedTags.join(', ') + '.');
    },

	_extractKeyWords: function(text) {
		var request = new sn_ws.RESTMessageV2('Keyword Extractor', 'POST');
		var requestBody = {
            sentences: [text]
        };
		request.setRequestBody(JSON.stringify(requestBody));

		var response;
        try {
            response = request.execute();
        } catch (ex) {
            gs.error('Error executing REST request: ' + ex.message);
            return [];
        }
    
        var responseBody = response.getBody();
        var httpStatus = response.getStatusCode();
        
        if (httpStatus == 200) {
            var parsedResponse = JSON.parse(responseBody);
            return parsedResponse.keywords[0]; //API returns an array of keywords
        } else {
            gs.error('Error in REST response: ' + httpStatus);
            return [];
        }

	},

    _getOrCreateTag: function(tagName) {
        var grTag = new GlideRecord('label');
        grTag.addActiveQuery();
        grTag.addQuery('name', tagName);
        grTag.addQuery('type', 'standard');
        grTag.addQuery('viewable_by', '!=', 'me');
        grTag.query();

        if (grTag.next()) {
            return grTag.getUniqueValue();
        } else {
            grTag.initialize();
            grTag.setValue('name', tagName);
            grTag.setValue('viewable_by', 'everyone');
            return grTag.insert();
        }
    },

    _addTagToRecord: function(tagSysId, tableName, recordId, recordNumber) {
        var grTagEntry = new GlideRecord('label_entry');
        grTagEntry.initialize();
        grTagEntry.setValue('label', tagSysId);
        grTagEntry.setValue('table', tableName);
        grTagEntry.setValue('table_key', recordId);
        grTagEntry.setValue('title', tableName.charAt(0).toUpperCase() + tableName.slice(1) + ' - ' + recordNumber);
        grTagEntry.insert();
    },


    type: 'AutoTagger'
};
