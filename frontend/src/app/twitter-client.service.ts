import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class TwitterClientService {
  private fakeApiUrl = 'http://138.197.144.15:8000/fakeanalyze?user_query=';
  private apiUrl = 'http://138.197.144.15:8000/analyze_many?type=recent';

  constructor(private http: HttpClient) {}

  getTestEntities(): Observable<any> {
    return this.http.get(this.fakeApiUrl);
  }

  getEntities(keywords: Array<string>): Observable<any> {
    var params = new HttpParams().set('keywords', keywords.join());
    return this.http.get(this.apiUrl, {params});
  }

  getEntity(keyword: string): Observable<any> {
    var params = new HttpParams().set('keywords', keyword);
    return this.http.get(this.apiUrl, {params});
  }

}
