/// <reference path="../../Scripts/typings/angularjs/angular.d.ts" />

'use strict';

module ReferenceModule {
    export class ReferenceDirective {
        constructor() {
            return this.CreateDirective();
        }
        private CreateDirective(): any {
            return {
                template: ''
                + '<table id="references">'
                +   '<thead>'
                +     '<tr>'
                +       '<th>住所</th>'
                +       '<th>築年</th>'
                +       '<th>面積(㎡)</th>'
                +       '<th>駅</th>'
                +       '<th>徒歩(分)</th>'
                +       '<th>掲載金額(万円)</th>'
                +     '</tr>'
                +   '</thead>'
                +   '<tbody>'
                +     '<tr ng-repeat="ref in response_howmuch.ref">'
                +       '<td>{{ref.address}}</td>'
                +       '<td>{{ref.year}}</td>'
                +       '<td>{{ref.occupiedArea}}</td>'
                +       '<td>{{ref.station}}</td>'
                +       '<td>{{ref.walkTime}}</td>'
                +       '<td>{{ref.price | number}}</td>'
                +     '</tr>'
                +   '</tbody>'
                + '</table>'
            }
        }
    }
}

angular.module('myApp').directive('referenceDirective', () => new ReferenceModule.ReferenceDirective());
