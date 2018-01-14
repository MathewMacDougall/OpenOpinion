import { Component, OnInit, ViewChild, AfterContentInit} from '@angular/core';

import { TwitterClientService } from './twitter-client.service';

import { WordSelectComponent } from './word-select/word-select.component';

import {Observable} from 'rxjs/Observable';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterContentInit{

  data: Array<any>;
  observable: Observable<any>;
  isLoading: boolean;

  @ViewChild(WordSelectComponent) wordSelect;

  constructor(
    private twitterDataService: TwitterClientService
  ) {}

  ngAfterContentInit() {
    this.requestData();
  }

  requestData = () => {
    console.log(this.wordSelect.keywords);

    if(this.wordSelect.keywords.length > 0) {
      this.isLoading = true;
      this.observable = this.twitterDataService.getEntities(this.wordSelect.keywords);
      this.observable.subscribe(data => this.handleData(data));
    } else {
      setTimeout(this.requestData, 5000);
    }
  }

  handleData = (data) => {
    this.data = data;
    this.isLoading = false;

    setTimeout(this.requestData, 5000);
  }
}
