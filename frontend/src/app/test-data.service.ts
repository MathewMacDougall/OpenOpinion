import { Injectable } from '@angular/core';

@Injectable()
export class TestDataService {
  generateData = (num: number) => {
    const results = [];
    const devices = ['Printer', 'Phone'];

    for (let i = 0; i < num; i++) {
      const result = {
        id: i,
        type: devices[Math.floor(Math.random() * devices.length)]
      };

      results.push(result);
    }

    return results;
  }
}
