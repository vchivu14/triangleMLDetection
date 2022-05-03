<script>
  import { onMount } from "svelte";
  import ResultBox from "./ResultBox.svelte";
  import { toast } from "@zerodevx/svelte-toast";

  let pointOne, pointTwo, pointThree;
  let board;
  let xylength;
  let yzlength;
  let zxlength;
  let area;
  let triangleType;

  let props = {
    xylength,
    yzlength,
    zxlength,
    area,
    triangleType,
  };

  function buildTriangle(x, y, z) {
    pointOne = board.create("point", [x[0], x[1]]);
    pointTwo = board.create("point", [y[0], y[1]]);
    pointThree = board.create("point", [z[0], z[1]]);

    board.create("arrow", [pointOne, pointTwo], {
      withLabel: true,
      label: { position: "top", parse: false },
      lastArrow: { type: 4, size: 8 },
    });
    board.create("arrow", [pointTwo, pointThree], {
      withLabel: true,
      label: { position: "top", parse: false },
      lastArrow: { type: 4, size: 8 },
    });
    board.create("arrow", [pointThree, pointOne], {
      withLabel: true,
      label: { position: "top", parse: false },
      lastArrow: { type: 4, size: 8 },
    });
  }

  function makeCalculations() {
    xylength = Number.parseFloat(determineLineLength(pointOne, pointTwo));
    yzlength = Number.parseFloat(determineLineLength(pointTwo, pointThree));
    zxlength = Number.parseFloat(determineLineLength(pointThree, pointOne));

    triangleType = determineTriangleType(xylength, yzlength, zxlength);

    area = Number.parseFloat(
      determineTriangleArea(xylength, yzlength, zxlength)
    );
  }

  function createBoard() {
    board = JXG.JSXGraph.initBoard("graphbox", {
      boundingbox: [-50, 50, 50, -50],
      showCopyright: false,
      showNavigation: false,
      axis: true,
    });
  }

  onMount(async () => {
    createBoard();

    buildTriangle([10, 10], [-10, 10], [-10, -10]);

    makeCalculations();

    getAttributesChanged();
  });

  function getAttributesChanged() {
    props.xylength = Number.parseFloat(determineLineLength(pointOne, pointTwo));
    props.yzlength = Number.parseFloat(
      determineLineLength(pointTwo, pointThree)
    );
    props.zxlength = Number.parseFloat(
      determineLineLength(pointThree, pointOne)
    );
    props.triangleType = determineTriangleType(
      props.xylength,
      props.yzlength,
      props.zxlength
    );
    props.area = Number.parseFloat(
      determineTriangleArea(props.xylength, props.yzlength, props.zxlength)
    );
  }

  function determineTriangleArea(x, y, z) {
    // formula
    // √(halfPerimeter * (halfPerimeter - x) * (halfPerimeter - y) * (halfPerimeter - z))
    const halfPerimeter = (x + y + z) / 2;
    const one = halfPerimeter - x;
    const two = halfPerimeter - y;
    const three = halfPerimeter - z;
    const result = halfPerimeter;
    result * one * two * three;
    return Math.sqrt(result).toFixed(2);
  }

  function determineTriangleType(x, y, z) {
    if ((x === y) === z) {
      return "equilateral";
    } else if (x === y || y === z || z === x) {
      return "isosceles";
    }
    return "scalene";
  }

  function determineLineLength(p1, p2) {
    // formula:
    // √[(x₂ - x₁)² + (y₂ - y₁)²]
    let x1 = p1.coords.usrCoords[1];
    let x2 = p2.coords.usrCoords[1];
    let y1 = p1.coords.usrCoords[2];
    let y2 = p2.coords.usrCoords[2];
    let eqFirstPart = Math.pow(x2 - x1, 2);
    let eqSecondPart = Math.pow(y2 - y1, 2);
    return Math.sqrt(eqFirstPart + eqSecondPart).toFixed(2);
  }

  let validCoords = [];
  function addCoord(coord) {
    let index = validCoords.findIndex((x) => x.name == coord.name);
    if (index === -1) {
      validCoords.push(coord);
    } else {
      validCoords[index].value = coord.value;
    }
  }

  function validateFormInput(e) {
    const coord = e.target;
    const variable = coord.name;
    let result = {};
    result.name = variable;
    if (
      e.target.value
        .toLowerCase()
        .match(
          /^([-+]?)([\d]{1,2})(((\.)(\d+)(,)))(\s*)(([-+]?)([\d]{1,3})((\.)(\d+))?)$/
        )
    ) {
      coord.style.color = "green";
      window[variable] = true;
      result.value = window[variable];
    } else {
      coord.style.color = "red";
      window[variable] = false;
      result.value = window[variable];
    }
    // console.log(result);
    // console.log(validCoords);
    addCoord(result);
  }

  function formInputTake() {
    const isValid = validCoords.every((item) => item.value === true);
    if (isValid && validCoords.length > 0) {
      let xVal = document.getElementById("xCoord").value.split(",");
      let yVal = document.getElementById("yCoord").value.split(",");
      let zVal = document.getElementById("zCoord").value.split(",");
      let x = [Number.parseFloat(xVal[0]), Number.parseFloat(xVal[1])];
      let y = [Number.parseFloat(yVal[0]), Number.parseFloat(yVal[1])];
      let z = [Number.parseFloat(zVal[0]), Number.parseFloat(zVal[1])];
      createBoard();
      buildTriangle(x, y, z);
      makeCalculations();
      getAttributesChanged();
    } else {
      toast.push("Input parameters have the wrong format, please update!");
    }
  }
</script>

<div class="container">
  <div class="row">

    <div class="col-md-8">
      <div id="graphbox" class="jxgbox graphbox" />
    </div>

    <div class="col-md-4">
      <div class="row">
        <div id="formbox" class="jxgbox formbox">
          <form on:submit|preventDefault={formInputTake}>
            <label for="xCoord">X Coords:</label><br />
            <input
              type="text"
              id="xCoord"
              name="xCoord"
              placeholder="10.00,10.00"
              on:input={validateFormInput}
            />
            <br />
            <label for="yCoord">Y Coords:</label><br />
            <input
              type="text"
              id="yCoord"
              name="yCoord"
              placeholder="-10.00,10.00"
              on:input={validateFormInput}
            />
            <br />
            <label for="zCoord">Z Coords:</label><br />
            <input
              type="text"
              id="zCoord"
              name="zCoord"
              placeholder="-10.00,-10.00"
              on:input={validateFormInput}
            />
            <hr />
            <button class="btn btn-warning" type="submit">Calculate</button>
          </form>
        </div>
      </div>

      <br>
      <div class="row">
        <button type="button" class="btn btn-success" style="float: left;" on:click={getAttributesChanged}>Determine</button>
      </div>
      <br>

      <div class="row">
        <div id="resultbox" class="jxgbox resultbox">
          <ResultBox {...props} />
        </div>
      </div>
    </div>

  </div>
</div>

<style>
  .graphbox {
    width: 600px;
    height: 600px;
  }
  .resultbox {
    width: 300px;
    height: 260px;
  }
  .formbox {
    width: 300px;
    height: 260px;
  }
</style>