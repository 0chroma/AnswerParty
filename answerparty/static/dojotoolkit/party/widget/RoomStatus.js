define("party/widget/RoomStatus", ["dojo", "party", "dijit/_Widget", "dijit/_Templated"], function(dojo, party) {

    dojo.declare("party.widget.RoomStatus", [dijit._Widget, dijit._Templated], {
        templateString: "<ul class='partyRoomStatus'></ul>",
        currentUser: "",

        addUser: function(name){
            var li = dojo.create("li", {innerHTML: name});
            this.domNode.appendChild(li);
        },
        clearList: function(){
            this.domNode.innerHTML = "";
        },

        markActiveUser: function(name){
            dojo.query("*", this.domNode).forEach(function(node){
                if(node.innerHTML == name){
                    dojo.addClass(node, "active");
                }else{
                    dojo.removeClass(node, "active");
                }
            });
        },

        updateList: function(list, nameActive){
            this.clearList();
            for(var i in list){
                this.addUser(list[i]);
            }
            this.markActiveUser(nameActive);
        }
        
    });

    return party.widget.RoomStatus;

});
