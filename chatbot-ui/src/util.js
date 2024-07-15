import isNil from "lodash/isNil";

export function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function isFalsy(value) {
  return !value || isNil(value);
}
