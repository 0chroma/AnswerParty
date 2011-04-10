define("party/widget/AnswerInput", ["dojo", "party", "dijit/_Widget", "dijit/_Templated"], function(dojo, party) {

    dojo.declare("party.widget.AnswerInput", [dijit._Widget, dijit._Templated], {
        templateString: dojo.cache("party.widget", "templates/AnswerInput.html"),
        sentence: "",
        inputShown: false,
        _stopSpace: function(e){
            if(dojo.keys.SPACE == e.keyCode){
                dojo.stopEvent(e);
            }
        },
        _setSentenceAttr: function(value){
            this.sentenceNode.innerHTML=value;
        },
        showInput: function(){
            this.inputShown=true;
            dojo.style(this.inputNode, "display", "inline");
            this.inputFieldNode.focus();
        },
        hideInput: function(){
            this.inputShown=false;
            dojo.style(this.inputNode, "display", "none");
        },
        sendWord: function(e){
            //sends the inputted word to the server and clears the textbox
            dojo.stopEvent(e);
            this.inputFieldNode.disabled = true;
            dojo.xhrPost({
                url: "/submitWord",
                handleAs: "json",
                content: {
                    word: "asdf"
                },
                load: dojo.hitch(this, function(){
                    this.hideInput();
                    this.inputFieldNode.disabled = false;
                }),
                error: function(){
                    alert("Problem sending your word, sorry!");
                }
            });
        }
    });

    return party.widget.AnswerInput;

});
