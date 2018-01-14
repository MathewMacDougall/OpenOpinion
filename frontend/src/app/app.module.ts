import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { SearchComponent } from './search/search.component';
import { GraphComponent } from './graph/graph.component';

import { TwitterClientService } from './twitter-client.service';
import { WordSelectComponent } from './word-select/word-select.component';


@NgModule({
  declarations: [
    AppComponent,
    SearchComponent,
    GraphComponent,
    WordSelectComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [TwitterClientService],
  bootstrap: [AppComponent]
})
export class AppModule { }
