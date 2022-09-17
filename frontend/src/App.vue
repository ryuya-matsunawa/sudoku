<template>
  <div id="app">
    <div>
      <table class="sudoku">
        <tr
          v-for="(line, lineIndex) in numbers"
          :key="lineIndex"
          :class="{
            'border-bottom': lineIndex == 2 || lineIndex == 5,
          }"
        >
          <td
            v-for="(number, numberIndex) in line"
            :key="numberIndex"
            :class="{
              'border-right': numberIndex == 2 || numberIndex == 5,
              'related-cell': relatedCell(lineIndex, numberIndex),
              selected:
                selectedCell.rowIndex == lineIndex &&
                selectedCell.columnIndex == numberIndex,
              'initial-value': inputArray[lineIndex][numberIndex],
            }"
            @click="selectCell(lineIndex, numberIndex)"
          >
            {{ number == 0 ? "" : number }}
          </td>
        </tr>
      </table>
      <div class="d-flex button-area">
        <button @click="resetCell">リセット</button>
        <button @click="resolve">自動回答</button>
      </div>
      <div
        v-if="hasAnotherSolution || !hasSolution"
        class="d-flex another-solution"
      >
        {{ message }}
      </div>
    </div>
    <div class="seletable-numbers">
      <button
        v-for="(number, i) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 'C']"
        :key="i"
        @click="setNumber(number)"
      >
        {{ number }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      numbers: [
        [0, 2, 3, 0, 0, 5, 0, 6, 0],
        [7, 0, 5, 0, 2, 0, 9, 0, 0],
        [0, 0, 0, 0, 7, 0, 0, 0, 4],
        [5, 8, 0, 0, 0, 0, 3, 0, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 0, 2, 0, 1, 0, 5, 0, 0],
        [0, 0, 0, 2, 9, 0, 0, 0, 0],
        [2, 3, 7, 0, 0, 8, 0, 0, 0],
        [0, 4, 1, 0, 0, 0, 0, 0, 0],
      ],
      selectedCell: {
        rowIndex: -1,
        columnIndex: -1,
      },
      inputArray: [...Array(9)].map(() => [...Array(9)]),
      hasAnotherSolution: false,
      hasSolution: true,
    };
  },
  computed: {
    relatedCell: function () {
      return function (lineIndex, numberIndex) {
        const isSelectedRow = lineIndex == this.selectedCell.rowIndex;
        const isSelectedColumn = numberIndex == this.selectedCell.columnIndex;
        const selectedCellBaseRow =
          Math.floor(this.selectedCell.rowIndex / 3) ==
          Math.floor(lineIndex / 3);
        const selectedCellBaseColumn =
          Math.floor(this.selectedCell.columnIndex / 3) ==
          Math.floor(numberIndex / 3);
        return (
          isSelectedRow ||
          isSelectedColumn ||
          (selectedCellBaseRow && selectedCellBaseColumn)
        );
      };
    },
    message() {
      if (this.hasAnotherSolution) {
        return "別解あるかも！";
      } else if (!this.hasSolution) {
        return "解がありません…";
      } else {
        return "";
      }
    },
  },
  methods: {
    selectCell(lineIndex, numberIndex) {
      this.selectedCell.rowIndex = lineIndex;
      this.selectedCell.columnIndex = numberIndex;
    },
    setNumber(selectedNumber) {
      if (this.selectedCell.rowIndex == -1) return;
      this.$set(
        this.numbers[this.selectedCell.rowIndex],
        this.selectedCell.columnIndex,
        selectedNumber == "C" ? 0 : selectedNumber
      );
    },
    resetCell() {
      this.numbers = [...Array(9)].map(() => [...Array(9)]);
    },
    resolve() {
      this.inputArray = this.numbers.map((line) =>
        line.map((number) => number != 0)
      );
      const path = "/api/resolve";
      axios
        .post(path, { numbers: this.numbers })
        .then((res) => {
          if (res.data.has_solution) {
            this.numbers = res.data.results[0];
            this.hasAnotherSolution = res.data.has_another_solution;
          }
          this.hasSolution = res.data.has_solution;
        })
        .catch((err) => err);
    },
  },
};
</script>

<style lang="scss">
#app {
  box-sizing: border-box;
  margin-top: 60px;
  display: flex;
  justify-content: center;
  .sudoku {
    margin-right: 20px;
    margin-bottom: 20px;
    border-collapse: collapse;
    border: 3px solid #ccc;
    td {
      border: 1px solid #ccc;
      height: 80px;
      width: 80px;
      text-align: center;
      vertical-align: middle;
      font-size: 55px;
      cursor: pointer;
    }
    .initial-value {
      color: blue;
    }
    .related-cell {
      background: rgba(243, 242, 170, 0.5);
    }
    .selected {
      background: rgba(245, 241, 44, 0.5);
    }
  }
  .button-area {
    margin-bottom: 15px;
    button {
      margin: 0 10px;
      padding: 10px 20px;
    }
  }
  .another-solution {
    color: red;
    font-size: 24px;
  }
  .seletable-numbers {
    display: flex;
    flex-direction: column;
    button {
      width: 50px;
      height: 50px;
      font-size: 24px;
      margin-bottom: 10px;
    }
  }
}
.border-bottom {
  border-bottom: 3px solid #ccc;
}
.border-right {
  border-right: 3px solid #ccc !important;
}
.d-flex {
  display: flex;
  justify-content: center;
}
</style>
