$.fn.dataTable.ext.type.order['difficulty-pre'] = function ( d ) {
   switch ( d ) {
  case '<span class="badge bg-very-easy">Very Easy></span>': return 1; 
  case '<span class="badge bg-easy">Easy</span>': return 2; 
  case '<span class="badge bg-medium">Medium</span>': return 3;
  case '<span class="badge bg-hard">Hard</span>': return 4;
  case '<span class="badge bg-very-hard">Very Hard</span>': return 5;
  case '': return 6; 
  } 
  return 0; }; 

$(document).ready(function() {
  $('#data-staff').DataTable( {
    "columnDefs": [
      { type: 'difficulty', "targets": 1 }
    ],
      "aoColumns": [
          { "bSortable": true },  // 0  
          { "bSortable": true },  // 1
          { "bSortable": true },  // 2
          { "bSortable": false },  // 3
      ]
  } );


  $('#data').DataTable( {
    "columnDefs": [
      { type: 'rank', targets: 1 }
    ],
      "aoColumns": [
          {
              "bSortable": true
          },
          {
              "bSortable": true
          },
          {
              "bSortable": true
          },
          {
              "bSortable": true
          }
      ]
  } );
});
