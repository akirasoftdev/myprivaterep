(function () {
    angular.module('myApp')

    .value('ErrorList', function() {
        return [
            {
                class: '10%未満',
                count: 3407,
                percentage: '14%'
            },
            {
                class: '20%未満',
                count: 7045,
                percentage: '30%'
            },
            {
                class: '30%未満',
                count: 10816,
                percentage: '46%'
            },
            {
                class: '40%未満',
                count: 14522,
                percentage: '62%'
            },
            {
                class: '50%未満',
                count: 17825,
                percentage: '77%'
            },
            {
                class: '60%未満',
                count: 19954,
                percentage: '86%'
            },
            {
                class: '70%未満',
                count: 21115,
                percentage: '91%'
            }
        ]
    })
})()
