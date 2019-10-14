class GameClient {
    constructor(url) {
	// you can get this code after registration on the server with your email
	//var url = "http://codenjoy.com:80/codenjoy-contest/board/player/3edq63tw0bq4w4iem7nb?code=1234567890123456789";
	this.path = url.replace("http", "ws").replace("board/player/", "ws?user=").replace("?code=", "&code=");
        this._map = new Board();
    }

    run(callback) {
        let _ = this
        this.socket = new WebSocket(this.path);
        this.socket.onopen = this.onOpen;
        this.socket.onerror = this.onError;
        this.socket.onclose = this.onClose;
        this.socket.onmessage = (event) => {
            _._map.update(event.data.substring(6));
            callback();
        }
    }

    get map() {
        return this._map;
    }

    onOpen() {
        text.value += "Connection established\n";
    }

    onClose(event) {
        if (event.wasClean) {
            text.value += "### disconnected ###\n"
        } else {
            text.value += "### accidentally disconnected ###\n";
            text.value += " - Err code: " + event.code + ", Reason: " + event.reason + "\n";
        }
    }

    onError(error) {
        text.value += "### error ###\n" + error.message + "\n";
    }

    send(msg) {
        text.value += "Sending: " + (msg?msg:'stop') + '\n'
        this.socket.send(msg)
    }

    up(fire = false) {
        this.send('(UP'+(fire?',ACT)':')'));
    }

    down(fire = false) {
        this.send('(DOWN'+(fire?',ACT)':')'));
    }

    right(fire = false) {
        this.send('(RIGHT'+(fire?',ACT)':')'));
    }

    left(fire = false) {
        this.send('(LEFT'+(fire?',ACT)':')'));
    }

    act() {
        this.send('(ACT)');
    }

    stop() {
        this.send('');
    }
}

class Board {

    constructor(){
        this._board = '';
    }

    update(_board) {
        this._board = _board;
        this._size = Math.sqrt(this._board.length);
        this._xyl = this.LengthToXY(); 
    }

    get size() {
        return this._size;
    }

    get getPlayerTank() {
        var result = [];
        result = result.concat(this.findAll(Element.TANK_UP));
        result = result.concat(this.findAll(Element.TANK_DOWN));
        result = result.concat(this.findAll(Element.TANK_LEFT));
        result = result.concat(this.findAll(Element.TANK_RIGHT));
        return result[0];
    }

    isAt(x, y, element) {
        if ((new Point(x, y)).isOutOf(this._size)) {
            return false;
        }
        return this.getAt(x, y) == element;
     }

    findAll(element) {
        let result = [];
        for (let i = 0; i < this._size*this._size; i++) {
            let point = this._xyl.getXY(i);
            if (this.isAt(point.x, point.y, element)) {
                result.push(point);
            }
        }
        return result;
    }

    getAt(x, y) {
		if ((new Point(x, y)).isOutOf(this._size)) {
           return Element.WALL;
        }
        return this._board.charAt(this._xyl.getLength(x, y));
    }

    LengthToXY() {
        let size = this._size;
        function inversionY(y) {
            return size - 1 - y;
        }
    
        function inversionX(x) {
            return x;
        }
        return {
            getXY : function(length) {
                if (length == -1) {
                    return null;
                }
                var x = inversionX(length % size);
                var y = inversionY(Math.ceil(length / size));
                return new Point(x, y);
            },
    
            getLength : function(x, y) {
                var xx = inversionX(x);
                var yy = inversionY(y);
                return yy*size + xx;
            }
        };
    }

    contains(a, obj) {
        var i = a.length;
        while (i--) {
           if (a[i].equals(obj)) {
               return true;
           }
        }
        return false;
    }

    removeDuplicates(all) {
        var result = [];
        for (var index in all) {
            var point = all[index];
            if (!contains(result, point)) {
                result.push(point);
            }
        }
        return result;
    }

    get getOtherPlayersTanks() {
        var result = [];
        result = result.concat(this.findAll(Element.OTHER_TANK_UP));
        result = result.concat(this.findAll(Element.OTHER_TANK_LEFT));
        result = result.concat(this.findAll(Element.OTHER_TANK_RIGHT));
        result = result.concat(this.findAll(Element.OTHER_TANK_DOWN));
        return result;
    }

    get getBotsTanks() {
        var result = [];
        result = result.concat(this.findAll(Element.AI_TANK_UP));
        result = result.concat(this.findAll(Element.AI_TANK_DOWN));
        result = result.concat(this.findAll(Element.AI_TANK_LEFT));
        result = result.concat(this.findAll(Element.AI_TANK_RIGHT));
        return result;
    }

    get getBullets() {
        var result = [];
        result.concat(this.findAll(Element.BULLET));
        return result;
    }

    get getConstructions() {
        var result = [];
        return result.concat(this.findAll(Element.CONSTRUCTION));
    }

    get getDestroyedConstructions() {
        var result = [];
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_DOWN));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_UP));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_LEFT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_RIGHT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_LEFT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_DOWN_TWICE));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_UP_TWICE));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_LEFT_TWICE));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_RIGHT_TWICE));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_DOWN_LEFT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_DOWN_RIGHT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_UP_LEFT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_UP_RIGHT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_LEFT_RIGHT));
        result = result.concat(this.findAll(Element.CONSTRUCTION_DESTROYED_UP_DOWN));
        return result;
    }

    get getWalls() {
        return this.findAll(Element.BATTLE_WALL);
    }

    get getBarriers() {
        var all = getConstructions;
        all = all.concat(this.getWalls);
        all = all.concat(this.getConstructions);
        all = all.concat(this.getDestroyedConstructions);
        all = all.concat(this.getOtherPlayersTanks);
        all = all.concat(this.getBotsTanks);
        return all;
    }

    get boardAsString() {
        var result = "";
        for (var i = 0; i < this._size; i++) {
            result += this._board.substring(i * this._size, (i + 1) * this._size);
            result += "\n";
        }
        return result;
    }

    printArray(array) {
        var result = [];
        for (var index in array) {
            var element = array[index];
            result.push(element.toString());
        }
        return "[" + result + "]";
    }

    toString() {
      return "Tank at: " + this.getPlayerTank + "\n"+
          "Other Tanks at: "+this.printArray(this.getOtherPlayersTanks)+"\n"+
          "Bot tanks at: "+this.printArray(this.getBotsTanks)+"\n"+
          this.boardAsString + "\n";
    }

   isAnyOfAt(x, y, elements) {
       for (var index in elements) {
           var element = elements[index];
           if (this.isAt(x, y,element)) {
               return true;
           }
       }
       return false;
   }

   isNear(x, y, element) {
       if ((new Point(x, y)).isOutOf(this._size)) {
           return false;
       }
       return this.isAt(x + 1, y, element) ||
            this.isAt(x - 1, y, element) ||
            this.isAt(x, y + 1, element) || 
            this.isAt(x, y - 1, element);
   }

   isBarrierAt(x, y) {
       return contains(this.getBarriers, new Point(x, y));
   }

   countNear(x, y, element) {
       if ((new Point(x, y)).isOutOf(this._size)) {
           return 0;
       }
       var count = 0;
       if (this.isAt(x - 1, y    , element)) count ++; // TODO to remove duplicate
       if (this.isAt(x + 1, y    , element)) count ++;
       if (this.isAt(x    , y - 1, element)) count ++;
       if (this.isAt(x    , y + 1, element)) count ++;
       return count;
   }
}

class Point {
    constructor(x,y){
        this._x = x;
        this._y = y;
    }
    
    equals(o) {
        return o.x() == this._x && o.y() == this._y;
    }

    toString() {
        return '[' + this._x + ',' + this._y + ']';
    }

    isOutOf(boardSize) {
        return this._x >= boardSize || this._y >= boardSize || this._x < 0 || this._y < 0;
    }

    get x() {
        return this._x;
    }

    get y() {
        return this._y;
    }
};