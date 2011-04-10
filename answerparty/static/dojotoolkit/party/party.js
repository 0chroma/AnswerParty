define("party", [], {});
define("party/party", ["dojo", "party", "party/widget/QuestionBlock", "party/widget/AnswerInput", "party/widget/RoomStatus"], function(dojo, party) {
    party = {
        start: function(){
            setInterval(dojo.hitch(party, "update"), 2000);
        },
        update: function(){
            dojo.xhrPost({
                url: "/update",
                handleAs: "json",
                load: function(results){
                    dijit.byId("roomStatus").updateList(results.userList, results.currUser);
                    dijit.byId("answerInput").attr("sentence", results.sentence);
                    var answerInput = dijit.byId("answerInput");
                    if(results.isMyTurn && !answerInput.inputShown){
                        answerInput.showInput();
                    }
                },
                error: function(){
                    //whatever
                }
            });
        },
        crash: function(){
            dojo.xhrGet({
                url: "/leave",
                async: true
            });
        }
    };
    
    dojo.addOnLoad(dojo.hitch(party, "start"));
    dojo.addOnUnload(dojo.hitch(party, "crash"));

    return party;

});
