export default function (removedIndex, addedIndex, arr) {
  let pos;
  if (addedIndex === arr.length - 1) {
    pos = parseInt(arr[arr.length - 1].pos) + 16384;
  } else if (addedIndex === 0) {
    pos = parseInt(arr[0].pos) / 2;
  } else if (addedIndex < removedIndex) {
    let beforePOS = parseInt(arr[addedIndex - 1].pos);
    let afterPOS = parseInt(arr[addedIndex].pos);

    pos = (beforePOS + afterPOS) / 2;
  } else if (addedIndex > removedIndex) {
    let beforePOS = parseInt(arr[addedIndex + 1].pos);
    let afterPOS = parseInt(arr[addedIndex].pos);

    pos = (beforePOS + afterPOS) / 2;
  }

  return pos;
}
