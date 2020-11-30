function diagonalDifference(arr) {
    let leftDiagonal = 0;
    let rigthDiagonal = 0;
    for(let n = 0; n <= arr.length - 1; n = n + 1 ){
        for(let j = 0; j <= arr.length - 1; j = j + 1 ){
            if(j === n){
                leftDiagonal = leftDiagonal + arr[n][j];
            }
            if(j === arr.length - n - 1){
                rigthDiagonal = rigthDiagonal + arr[n][j];
            }
        }
    }
    let plusDiagonal = leftDiagonal - rigthDiagonal;
    return plusDiagonal < 0? -plusDiagonal: plusDiagonal;
}

console.log(diagonalDifference([[11, 2, 4],[4, 5, 6],[10, 8, -12]]));