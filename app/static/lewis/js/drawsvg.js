
function scaleX(x){
    return (x+1)*200+200
}

function scaleY(y){
    return (y+1)*125+150
}
function drawAtom(symbol, x, y) {
    const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle"
    );

    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", 40);
    circle.setAttribute("fill", "white");
    circle.setAttribute("stroke", "black");

    svg.appendChild(circle);
    const atom = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "text"
    );

    atom.setAttribute("x", x);
    atom.setAttribute("y", y+10);
    atom.setAttribute("class", "atom");
    atom.textContent = symbol;

    svg.appendChild(atom);
}

function drawBond(x1, y1, x2, y2, order = 1) {
    const spacing = 6;
    order = order/2
    if (order === 1) {
        createLine(x1, y1, x2, y2);
    }
    else if (order === 2) {
        createLine(x1, y1 - spacing, x2, y2 - spacing);
        createLine(x1, y1 + spacing, x2, y2 + spacing);
    }
    else if (order === 3) {
        createLine(x1, y1, x2, y2);
        createLine(x1, y1 - spacing, x2, y2 - spacing);
        createLine(x1, y1 + spacing, x2, y2 + spacing);
    }
}

function createLine(x1, y1, x2, y2) {
    const line = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line"
    );

    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);
    line.setAttribute("class", "bond");

    svg.appendChild(line);
}

function drawElectronPair(x, y) {
    drawElectron(x - 13, y);
    drawElectron(x + 13, y);
}

function drawElectron(x, y) {
    const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle"
    );

    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", 5);
    circle.setAttribute("class", "electron");

    svg.appendChild(circle);
}
function line(x1,y1,x2,y2){

    const l = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "line"
    );

    l.setAttribute("x1",x1);
    l.setAttribute("y1",y1);
    l.setAttribute("x2",x2);
    l.setAttribute("y2",y2);

    l.setAttribute("stroke","black");
    l.setAttribute("stroke-width","3");

    svg.appendChild(l);
}
function electron(x,y){

    const c = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle"
    );

    c.setAttribute("cx",x);
    c.setAttribute("cy",y);
    c.setAttribute("r",2);

    svg.appendChild(c);
}
function occupiedDirections(node, nodes, edges) {

    const dirs = [];

    const neighbors = edges
        .filter(e =>
            e.source === node.id ||
            e.target === node.id
        );

    for (const edge of neighbors) {

        const id =
            edge.source === node.id
                ? edge.target
                : edge.source;

        const other =
            nodes.find(n => n.id === id);

        const dx = other.x - node.x;
        const dy = other.y - node.y;

        let dir;

        if (Math.abs(dx) > Math.abs(dy)) {
            dir = dx > 0 ? "E" : "W";
        } else {
            dir = dy > 0 ? "S" : "N";
        }

        dirs.push(dir);
    }

    return dirs;
}
function drawMolecule(nodes, edges) {
    svg.replaceChildren();
    edges.forEach(edge => {

        const n1 = nodes.find(n => n.id === edge.source);
        const n2 = nodes.find(n => n.id === edge.target);

        const x1 = scaleX(n1.x);
        const y1 = scaleY(n1.y);

        const x2 = scaleX(n2.x);
        const y2 = scaleY(n2.y);
        drawBond(x1,y1,x2,y2, edge.weight)
        

    });
    nodes.forEach(node => {
        drawAtom(node['elemento'], scaleX(node['x']), scaleY(node['y']));
        let count = Math.round(node.free_atoms);
        const x = scaleX(node['x']);
        const y = scaleY(node['y']);

        const adjust_ = {
            "W": [50,0],
            "E": [-50,0],
            "N": [0,50],
            "S": [0,-50]
        };
        const occupied =
        occupiedDirections(
            node,
            nodes,
            edges
        );
        const possible =
            ["N","S","E","W"]
            .filter(
                d => !occupied.includes(d)
        );
        possible.forEach(function(direc) {
            if (count>=2){
                count -=2;
                drawElectronPair(x + adjust_[direc][0], y + adjust_[direc][1]);
            }
        });
    });
}


