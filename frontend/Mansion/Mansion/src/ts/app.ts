/// <reference path="_include.ts" />
module app {
    var module = angular.module('app', ['ngResource', 'toastr']);
    module.component('referenceComponent', ReferenceComponentFactory());
    module.component('priceComponent', PriceComponentFactory());
    module.component('postComponent', PostComponentFactory());
    module.component('errorComponent', ErrorComponentFactory());
}
