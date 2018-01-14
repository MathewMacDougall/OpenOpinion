import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-word-select',
  templateUrl: './word-select.component.html',
  styleUrls: ['./word-select.component.scss']
})
export class WordSelectComponent implements OnInit {

  keywords: Array<string> = ['UBC', 'SFU', 'UofT'];
  addKeywordValue: string;

  constructor() { }

  ngOnInit() {
  }

  onEnter(value: string) {
    this.addKeywordValue = "";

    if(!value || value.length == 0) {
      return;

    }

    if(this.keywords.indexOf(value) >=0) {
      return;
    }

    this.keywords.push(value);
  }

  onClick(value: string) {
    this.keywords.splice(this.keywords.indexOf(value), 1);
  }

}
