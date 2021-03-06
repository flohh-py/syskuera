$(document).ready(function() {
  $("#id_item").select2({
    dropdownParent: $('#itemModal'),
    ajax: {
      url: "/product/",
      dataType: "json",
      processResults: function(data) {
        return {
          results: $.map(data, function(r) {
            return { id: r.id, text: r.code };
          })
        };
      }
    },
    minimumInputLength: 2
  });
  $("#id_item").on("select2:select", function(e) {
    $.ajax({
      type: "GET",
      url: "/product/detail/" + $("#id_item").select2('data')[0].id
    }).then(function(data) {
      $("#id_qty").val(1.0)
      $("#id_price").val(data.price)
    })
  })
  $("#id_partner").select2({
    // dropdownParent: $('#itemAddModal'),
    ajax: {
      url: "/partner/",
      dataType: "json",
      data: function name(params) {
        invo_type = $("#id_type").val()
        return {
          type: invo_type,
          term: params.term
        }
      },
      processResults: function(data) {
        return {
          results: $.map(data, function(r) {
            return { id: r.id, text: r.name };
          })
        };
      }
    },
    minimumInputLength: 2
  });
});
function edit_line(id) {
  $.get("/invoice/edit_line/" + id, function(data) {
    $("#item-modal-content").html(data)
  })
  $("#itemModal").modal("toggle");
}
function add_line(id) {
  $.get("/invoice/add_line/", function(data) {
    $("#item-modal-content").html(data)
    $("#id_parent").val(id) //gambiarra?
  })
  $("#itemModal").modal("toggle");
}
function delete_line(id) {
  $.get("/invoice/delete_line/" + id, function(data) {
    $("#item-modal-content").html(data)
  })
  $("#itemModal").modal("toggle");
}
function create_ste(invo_id) {
  console.log("CREATE_STE")
  // $("#itemModal").modal("toggle");
  $.get("/invoice/create_stockentry/" + invo_id, function(data) {
    $("#item-modal-content").html(data)
  })
  // $("#itemModal").modal("toggle");
}
function list_ste(invo_id) {
  $.get("/invoice/list_stockentry/" + invo_id, function(data) {
    $("#item-modal-content").html(data)
    // $("#item-modal-content").modal({ backdrop: 'static', keyboard: false })
  })
  $("#itemModal").modal("toggle");
}
