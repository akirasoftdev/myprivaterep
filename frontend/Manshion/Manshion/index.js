var hostName = ''

function onInit() {
  document.getElementById('predict').onclick = onAddress
  var year_text = document.getElementById('year')
  var occupied_text = document.getElementById('occupied')
  var walk_text = document.getElementById('walk')
}

function verifyYear(year) {
  return (year != "")
}

function verifyOccupied(occupied) {
  return (occupied != "")
}

function verifyWalk(walk) {
  return (walk != "")
}

function onPredict() {
  var year = document.getElementById('year').value
  var occupied = document.getElementById('occupied').value
  var walk = document.getElementById('walk').value
  var town = document.getElementsByName('addr21')[0].value

  clearReferences()

  var in_data = {}
  if (verifyYear(year)) {
    in_data['year'] = year
  }
  if (verifyOccupied(occupied)) {
    in_data['occupied'] = occupied
  }
  if (verifyWalk(walk)) {
    in_data['walk'] = walk
  }
  in_data['town_id'] = town
  $.ajax({
    type: 'GET',
    url: hostName + '/address',
    contentType: 'application/json',
    data: JSON.stringify({
      "data": in_data
    }),
    dataType: 'json',
    success: function(json) {
      console.log(json)
    }
  });
}

function onAddress() {
  town = document.getElementsByName('addr21')[0].value
  address = town
  year = document.getElementById('year').value
  occupied = document.getElementById('occupied').value
  walk = document.getElementById('walk').value

  clearReferences()

  $.ajax({
    type: 'GET',
    url: hostName + '/howmuch?address=' + address + '&year=' + year + '&occupied=' + occupied + '&walk=' + walk,
    contentType: 'application/json',
    datatType: 'json',
    success: function(results) {
      console.log(results)
      var json = $.parseJSON(results)
      document.getElementById('price').value = json['price'].toLocaleString()
      document.getElementById('low').value = json['low'].toLocaleString()
      document.getElementById('high').value = json['high'].toLocaleString()
      for (key in json['ref']) {
        addReference(
            json['ref'][key]['address'],
            json['ref'][key]['year'],
            json['ref'][key]['occupiedArea'] / 100,
            json['ref'][key]['station'],
            json['ref'][key]['walkTime'],
            json['ref'][key]['price'].toLocaleString()
        )
      }
    },
    error: function(response) {
        alert(response.responseText)
    }
  })
}

function clearReferences() {
    var referenceTable = document.getElementById('references')
    var tbody = referenceTable.getElementsByTagName('tbody')[0]
    while (tbody.firstChild) tbody.removeChild(tbody.firstChild)
}

function addReference(address, year, occupiedArea, station, walk, price) {
    var referenceTable = document.getElementById('references')
    var tbody = referenceTable.getElementsByTagName('tbody')[0]
    var tr = tbody.insertRow(-1);

    var td = tr.insertCell(-1);
    var addressNode = document.createTextNode(address)
    td.appendChild(addressNode)

    var td = tr.insertCell(-1);
    var yearNode = document.createTextNode(year)
    td.appendChild(yearNode)

    var td = tr.insertCell(-1);
    var occupiedAreaNode = document.createTextNode(occupiedArea)
    td.appendChild(occupiedAreaNode)

    var td = tr.insertCell(-1);
    var stationNode = document.createTextNode(station)
    td.appendChild(stationNode)

    var td = tr.insertCell(-1);
    var walkNode = document.createTextNode(walk)
    td.appendChild(walkNode)

    var td = tr.insertCell(-1);
    var priceNode = document.createTextNode(price)
    td.appendChild(priceNode)
}

