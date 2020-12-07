#!/usr/bin/node

const fs = require('fs');
const util = require('util');

const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

const input = fs.readFileSync('input.txt', 'utf8');

const main = async (addBy = { x: 3, y: 1 }) => {
	//console.log(input);
	const charMap = input.split('\n').map(l => l.split('')).filter(Boolean).filter(r => r.length);
	const treeMap = charMap.map(r => r.map(c => c == '#'));
	const mapHeight = charMap.length;
	const mapWidth = Math.min(...charMap.map(r => r.length));
	// console.log(`mapHeight: ${mapHeight}, mapWidth: ${mapWidth}`);
	// const addBy = { x: 3, y: 1 };
	let pos = { x: 0, y: 0 };
	let numTreesHit = 0;
	let numMisses = 0;

	const outputCharMap = charMap.map(r => r.slice());
	const realOutputCharMap = charMap.map(r => r.slice());
	const positions = []

	while (pos.y < mapHeight) {
		const fakePosX = pos.x % mapWidth
		const isAtTree = treeMap[pos.y][fakePosX]
		if (isAtTree) numTreesHit++;
		else numMisses++;
		outputCharMap[pos.y][fakePosX] = isAtTree ? 'X' : 'O';
		positions.push({x: pos.x, y: pos.y, isTree: isAtTree})
		// console.log(`[${pos.x}][${pos.y}]: ${isAtTree}`)
		pos.x += addBy.x
		pos.y += addBy.y
	}
	// console.log(`Tree hits: ${numTreesHit}, missed: ${numMisses}`);
	// const outputString = outputCharMap.map(r => r.join('')).join('\n')
	// await writeFile('output.txt', outputString);
	return { numMisses, numTreesHit, positions, outputCharMap }
}	

//main();

const multipleTests = async () => {
	const tests = [
		{ x: 1, y: 1 },
		{ x: 3, y: 1 },
		{ x: 5, y: 1 },
		{ x: 7, y: 1 },
		{ x: 1, y: 2 },
	]
	let accumulativeProduct = 1;
	for (test of tests) {
		const { numTreesHit } = await main(test);
		console.log(`Test 1, trees hit: ${numTreesHit}`);
		accumulativeProduct = accumulativeProduct * numTreesHit;
	}
	console.log('Product: ' + accumulativeProduct)
}

multipleTests();
