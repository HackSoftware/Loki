$(document).ready(function () {
  function makeRequest(value, cb) {
    $.ajax({
      url: '/base/api/education-place-suggest/',
      type: "POST",
      data: {
          query: value
      },
      success: function (data) {
        cb(data);
      }
    });
  }

  function setSuggestionDropdown() {
    var suggestionDropdown = $("<div id='suggestion-dropdown'><ul></ul></div>");
    $("#id_studies_at").val("").after(suggestionDropdown);
    var field = $("#id_studies_at").clone();
    field.attr("name", '');
    field.attr('id', 'fuzzy-field');
    field.attr('autocomplete', 'off');
    $("#id_studies_at").hide().after(field);
    $("#id_education_info").hide();

    suggestionDropdown = suggestionDropdown.find("ul");

    return suggestionDropdown;
  }

  function fuzzysearchNavigation(keycode) {
    var el = $("#suggestion-dropdown .selected");
    if (keycode == 38) { // up
      if (el.prev().length > 0) {
          el.prev().addClass("selected");
          el.removeClass("selected");
      }
      return true;
    }

    if (keycode == 40) { // down
      if (el.next().length > 0) {
        el.next().addClass("selected");
        el.removeClass("selected");
      }
      return true;
    }

    if (keycode == 13) {
      selectItem();
      return true;
    }

    return false;
  }

  function selectItem() {
      // if an item from suggestion is selected - fill the ed_info field
      var el = $("#suggestion-dropdown .selected");
      var rawData = el.attr('ref');
      var data = JSON.parse(rawData);

      if(data !== false) {
        $("#id_education_info").val(rawData);
        $("#fuzzy-field").val(el.html().trim());
        $("#id_studies_at").val("");
        $("#suggestion-dropdown").hide();
      } else {
        var other = {
          other: $("#fuzzy-field").val()
        };

        $("#id_education_info").val(JSON.stringify(other));
        $("#suggestion-dropdown").hide();
      }

      if (el.attr('ref')) {
      } else {
          // if the "other thing" option is selected from the dropdown - fill in the "studies at" field
          if (el.attr("rel")) {
          }
      }
  }

  function represent(el) {
    var parts = [el.subject, el.faculty, el.educationplace, el.city];
    return _.compact(parts).join(" ");
  }


  $('.dateinput').datepicker({
    dateFormat: "dd-mm-yy",
    changeMonth: true,
    changeYear: true,
    showButtonPanel: true,
    onChangeMonthYear: function (year, mohth, inst) {
      $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
    },
    onClose: function (dateText, inst) {
      $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
    }
  });

  // preset the data because django datefield doesnt support placeholders
  $(".dateinput#id_start_date").attr("placeholder", "Учене от");
  $(".dateinput#id_end_date").attr("placeholder", "Учене до");

  var suggestionDropdown = setSuggestionDropdown();
  var timeout = false;

  $("#fuzzy-field").keyup(function(e) {
    if(fuzzysearchNavigation(e.which)) {
      e.preventDefault();
      return;
    }

    if(!timeout) {
      timeout = setTimeout(function() {
        $("#suggestion-dropdown").show();
        var value = $("#fuzzy-field").val().trim();

        if (value === "") {
          $("#suggestion-dropdown").hide();
          suggestionDropdown.html("");
          timeout = false;
          return;
        }

        makeRequest(value, function(data) {
          timeout = false;
          suggestionDropdown.html("");

          data.result.forEach(function(item, index) {
            var repr = represent(item);
            suggestionDropdown.append($("<li ref='" + JSON.stringify(item) + "'>" + repr + "</li>"));

          });

          suggestionDropdown.find("li").first().addClass('selected');
          suggestionDropdown.append($("<li ref='false'>" + "<b>Не намирам моето</b>" + "</li>"));
        });
      }, 1000);
    }
  });

  $(".register-form").submit(function (e) {
    if ($(":focus").is($("#fuzzy-field"))) {
      e.preventDefault();
      return;
    }
  }).on("mouseover", "#suggestion-dropdown li", function () {
    $("#suggestion-dropdown .selected").removeClass("selected");
    $(this).addClass("selected");
  }).on("click", "#suggestion-dropdown li", function () {
    selectItem();
  });

  $(document).click(function (e) {
    if (!$(e.target).is("#suggestion-dropdown")) {
      $("#suggestion-dropdown").hide();
    }
  });
});
