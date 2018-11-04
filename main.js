window.onload = start;
var requestedPlayer;
var requestedTeam;
var requestedDate;

function start() {


    var selectionContainer = d3.select('body').append('div').attr('class','container')
    .append('div').attr('class','row').attr('id','selectionRow');
    // var selectionRowText = selectionContainer.append('div').attr('class','col-sm-3').attr('id', 'Explain');
    var selectionRowTextbox = selectionContainer
        .append('div').attr('class','col-sm-3').attr('id', 'teamInputDiv');
    var selectionRowButton = selectionContainer
        .append('div').attr('class','col-sm-3').attr('id', 'teamInputButtonDiv');
    // var selectionRowDropDown = selectionContainer
    //     .append('div').attr('class','col-sm-3').attr('id', 'teamDropdownDiv');
    var selectionRowPlayerDropDown = selectionContainer
        .append('div').attr('class','col-sm-3').attr('id', 'playerDropdownDiv');
    var selectionRowButton = selectionContainer
        .append('div').attr('class','col-sm-3').attr('id', 'updateButtonDiv');
    
    // var teamDropdown = selectionRowDropDown.append('select').attr('id','teamDropdown');
    requestedPlayer = 'B_Burns';
    requestedTeam = 'North_Carolina';
    // d3.select('#team_name').append('h2').text(requestedTeam);
    // d3.select('#player_name').append('h2').text(requestedPlayer);
    // // requestedDate = ';
    // d3.csv('s.csv', function (error,data) {
    //     data.forEach(function(d) {
    //         teamDropdown.append('option').attr('value', d.code).text(d.team);
    //     })

    // });

    var teamInput = selectionRowTextbox.append('input').attr('type','text').attr('id','teamInputValue').attr('value',requestedTeam);


// var teamInputDropdown = selectionRowTextbox.append('select').attr('id','teamInputDropdown');
//     d3.csv('ers_' + requestedTeam + '.csv', function (error,data) {
//     data.forEach(function(d) {
//         teamInputDropdown.append('option').attr('value', d.Name).text(d.Name);
//     });
// });
        // .append('div').attr('class','col-sm-3').attr('id', 'updateButtonDiv');


    // <form action="/action_page.php">
    //     First Name: <input type="text" Name="FirstName" value="Mickey"><br>
    //     Last Name: <input type="text" Name="LastName" value="Mouse"><br>
    //     <input type="submit" value="Submit">
    // </form>


    var playerDropdown = selectionRowPlayerDropDown.append('select').attr('id','playerDropdown');
    // requestedTeam = d3.select('#teamInputValue').node().value;
    d3.csv(requestedTeam + '/players.csv', function (error,data) {
        data.forEach(function(d) {
            playerDropdown.append('option').attr('value', d.Name).text(d.Name);
        });
    });
    // playerDropdown.attr('value','B_Burns');



    var playerChanged = document.getElementById('playerDropdown');
    playerChanged.onchange = function() {
        requestedPlayer = d3.select("#playerDropdown").node().value;
        console.log('changed to: ' + requestedPlayer);
    };


    // var teamChanged = document.getElementById('teamDropdown');
    // teamChanged.onchange = function() {
    //     var requestedTeam = d3.select("#teamDropdown").node().value;
    //     alert(requestedTeam);
    //     playerDropdown.selectAll('*').remove();
    //     d3.csv('ers_' + requestedTeam + '.csv', function (error,data) {
    //         data.forEach(function(d) {
    //             playerDropdown.append('option').attr('value', d.Name).text(d.Name);
    //         });
    //     });
    // };
    // var updateButton = selectionRowPlayerDropDown.append('select').attr('id','updateButton');
    d3.select('#updateButtonDiv').append('button').text('Update Report')
    .on('click',function() {
        table1.selectAll('*').remove();
        requestedPlayer = d3.select("#playerDropdown").node().value;
        requestedTeam = requestedTeam.replace(" ", "_");
        requestedTeam = requestedTeam.replace(".", "");
        requestedPlayer = requestedPlayer.replace(" ", "_");
        requestedPlayer = requestedPlayer.replace(".", "");
        console.log('requested' + requestedPlayer);
        d3.csv(requestedTeam + '/' + requestedPlayer + '.csv', function (error,data) {

            // render the table(s)
            // tabulate(table1, data, ['data', 'close']); // 2 column table
            tabulate(table1,data, ['x','center','left','right','first','second','third','N/A','to ss','to pitcher']);

        });
    })


    d3.select('#teamInputButtonDiv').append('button').text('Update Players')
    .on('click',function() {
        requestedTeam = d3.select('#teamInputValue').node().value;
        requestedTeam = requestedTeam.replace(" ", "_");
        console.log('changed team Name to: ' + requestedTeam);
        // table1.selectAll('*').remove();
        d3.csv(requestedTeam + '/players.csv', function (error,data) {
            playerDropdown.selectAll('*').remove();
            data.forEach(function(d) {
            playerDropdown.append('option').attr('value', d.Name).text(d.Name);
        });

        });
    })


// var playerDropdown = selectionRowPlayerDropDown.append('select').attr('id','playerDropdown');
//     requestedTeam = d3.select('#teamInputValue').node().value;
//     d3.csv('dataplayers_' + requestedTeam + '.csv', function (error,data) {
//         data.forEach(function(d) {
//             playerDropdown.append('option').attr('value', d.Name).text(d.Name);
//         });
//     });




    // d3.select('#teamInputButtonDiv').append('button').text('Update Team')
    // .on('click',function() {
    //     table1.selectAll('*').remove();
    //     d3.csv('ers_gt.csv', function (error,data) {

    //         // render the table(s)
    //         // tabulate(table1, data, ['data', 'close']); // 2 column table

    //     });
    // })
    // update onClick
    // selectionRowUpdate
    // .append('button')
    // .text('Update Report')
    // .on('click', function() {
    //     table1.selectAll('tr')
    //     var row = table1.select("tbody").selectAll("tr")
    //         .data('data2.csv');
    //     row.exit().remove();
    //     row.append('tr');
    //     row.transition().duration(100)
    //         .append()


    //     // bars.selectAll('.bar')
    //     //     .filter(function(d) {
    //     //         // return d.frequency > 0.05;
    //     //         return d.frequency >= d3.select("#filterCutoff").node().value;
    //     //     })
    //     //     .transition()
    //     //     .duration(function(d) {
    //     //         return Math.random() * 1000;
    //     //     })
    //     //     .delay(function(d) {
    //     //         return d.frequency * 8000
    //     //     })
    //     //     .style('fill', d3.select("#colorDropdown").node().value)
    //     //     .attr('width', function(d) {
    //     //         // return xScale(d.frequency) / 2;
    //     //         return xScale(d.frequency);
    //     //     });
    //     // bars.selectAll('.bar')
    //     //     .filter(function(d) {
    //     //         // return d.frequency > 0.05;
    //     //         return d.frequency < d3.select("#filterCutoff").node().value;
    //     //     })
    //     //     .transition()
    //     //     .duration(function(d) {
    //     //         return Math.random() * 1000;
    //     //     })
    //     //     .delay(function(d) {
    //     //         return d.frequency * 8000
    //     //     })
    //     //     .style('fill', 'red')
    //     //     .attr('width', function(d) {
    //     //         // return xScale(d.frequency) / 2;
    //     //         return 0;
    //     //     });
    // });


    // var selectionContainer = d3.select('body').append('div').attr('class','container')
    // .append('div').attr('class','row').attr('id','selectionRow');
    // var selectionRowText = selectionContainer.append('div').attr('class','col-lg-12').attr('id', 'Explain');

    // var table1 = d3.select('body').append('table');
    table1 = d3.select('body').append('div').attr('class','container')
    .append('div').attr('class','row').attr('id','selectionRow')
    .append('div').attr('class','col-lg-12').attr('id', 'table1')
    .append('table');
    // requestedPlayer = d3.select("#playerDropdown").node().value;
    // d3.csv(requestedTeam + '/'+ requestedPlayer + '.csv', function (error,data) {


    //     // render the table(s)
    //     // tabulate(table1, data, ['date', 'close']); // 2 column table
    //     tabulate(table1,data, ['x','center','left','right','first','second','third','N/A','to ss','to pitcher']);


    // });


    // var table2 = d3.select('body').append('table');
    // var table2 = d3.select('body').append('div').attr('class','container')
    // .append('div').attr('class','row').attr('id','table1Row')
    // .append('div').attr('class','col-lg-12').attr('id', 'table2')
    // .append('table');

    // d3.csv('.csv', function (error,data) {
    //     // render the table(s)
    //     // tabulate(table2, data, ['date', 'close']); // 2 column table
    //     tabulate(table1,data, ['x','center','left','right','first','second','third','N/A','to ss','to pitcher']);


    // });

    function tabulate(position, data, columns) {
        // var table = d3.select('body').append('table')
        position.attr('class', 'table table-hover table-bordered table-striped')
        var thead = position.append('thead')
        var tbody = position.append('tbody');

        // append the header row
        thead.append('tr')
          .selectAll('th')
          .data(columns).enter()
          .append('th')
            .text(function (column) { return column; });

        // create a row for each object in the data
        var rows = tbody.selectAll('tr')
          .data(data)
          .enter()
          .append('tr');

        // create a cell in each row for each column
        var cells = rows.selectAll('td')
          .data(function (row) {
            return columns.map(function (column) {
              return {column: column, value: row[column]};
            });
          })
          .enter()
          .append('td')
            .text(function (d) { return d.value; });

          return position;
        };


}




