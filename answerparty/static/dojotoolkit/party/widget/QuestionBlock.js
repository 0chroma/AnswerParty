define("party/widget/QuestionBlock", ["dojo", "party", "dijit/_Widget", "dijit/_Templated"], function(dojo, party) {

    dojo.declare("party.widget.QuestionBlock", [dijit._Widget, dijit._Templated], {
        templateString: dojo.cache("party.widget", "templates/QuestionBlock.html"),
        postCreate: function(){
            this.inherited(arguments);
            this.showLoading();
            this.joinRoom();
        },
        _name: "",
        question: "",
        joinRoom: function(){
            if(!this._name){
                return this.getName();
            }
            this.showLoading()
            dojo.xhrPost({
                url: "/join",
                handleAs: "json",
                data: {
                    name: this._name
                },
                context: this,
                load: function(result){
                    this._name = result.name;
                    this.attr("question", result.question);
                },
                error: function(){
                    alert("There was a problem getting a question, sorry!");
                }
            });
        },
        showLoading: function(){
            this.attr("question", "Loading new question...");
        },
        getName: function(){
            dojo.style(this.nameFormNode, "display", "block");
            dojo.style(this.displayNode, "display", "none");
        },
        getNameInput: function(){
            this._name = this.nameFieldNode.value;
            dojo.style(this.nameFormNode, "display", "none");
            dojo.style(this.displayNode, "display", "block");
            this.joinRoom();
        },
        _setQuestionAttr: function(value){
            //TODO: if I have time, make this fade
            this.displayNode.innerHTML = value;
        }
    });

    return party.widget.QuestionBlock;

});
