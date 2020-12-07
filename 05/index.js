#!/usr/bin/node

const fs = require('fs');

const input = fs.readFileSync('input.txt', 'utf8');
const inputLines = input.split('\n').filter(Boolean);

const numRows = inputLines.length

const numSeatRows = 128;
const numSeatCols = 8;
const numSeats = numSeatRows * numSeatCols;

const seatsTaken = Array.from(new Array(numSeatRows), x => Array.from(new Array(numSeatCols), y => false));

// console.log(`Number of rows: ${numRows}`);

let highestSeatID = 0;

for (line of inputLines) {
	const rowString = line.substring(0, 7);
	const rowActions = rowString.split('').map((c, i) => c == 'F' ? -numSeatRows / 2**(i+1) : 0)
	const row = rowActions.reduce((a, c) => a + c, numSeatRows-1);
	
	const colString = line.substring(7, 10);
	const colActions = colString.split('').map((c, i) => c == 'L' ? -numSeatCols / 2**(i+1) : 0)
	const col = colActions.reduce((a, c) => a + c, numSeatCols-1);
	
	const seatID = row * 8 + col;
	
	seatsTaken[row][col] = true;
	// console.log({row, col, seatID});
	highestSeatID = Math.max(highestSeatID, seatID);
}	

const onlyFreeSeats = [].concat(...seatsTaken.map((row, y) => row.map((col, x) => !col ? {x,y} : false).filter(Boolean)).filter(r => r.length))

let filteredFirstFreeSeats = false;
const skipFirstFreeSeats = onlyFreeSeats.filter(({ x, y }, i) => {
	if ( x + y * numSeatCols != i ) filteredFirstFreeSeats = true;
	return filteredFirstFreeSeats;
});

let filteredLastFreeSeats = false;
const skipLastFreeSeats = skipFirstFreeSeats.reverse().filter(({ x, y }, i) => {
	if ( x + y * numSeatCols != numSeats - i - 1) filteredLastFreeSeats = true;
	return filteredLastFreeSeats;
});

/*
let passedFirstFreeSeats = false;
for (let yy = 0; yy < numSeatRows; yy++) {
	if (passedFirstFreeSeats) break;
	for (let xx = 0; xx < numSeatCols; xx++) {
		const { x, y } = onlyFreeSeats[ xx + yy * numSeatCols ];
		if (x != xx || y != yy) passedFirstFreeSeats = true;
		if (passedFirstFreeSeats) break;
		onlyFreeSeats[ xx + yy * numSeatCols ] = false;
	}
}
*/

// console.log(seatsTaken);
// console.log(onlyFreeSeats);
// console.log(seatsTaken.length);
const freeSeats = skipLastFreeSeats.map(({ x, y }) => ({ x, y, id: y * 8 + x }))
console.log(`Free seats: ${JSON.stringify(freeSeats)}`);
console.log(``);
console.log(`Highest seat ID: ${highestSeatID}`);
