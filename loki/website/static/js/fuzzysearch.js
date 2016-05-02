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
      var el = $("#suggestion-dropdown .selected");
      var rawData = el.attr('ref');
      var data = JSON.parse(rawData);

      $("#id_studies_at").val($("#fuzzy-field").val());

      if(!_.isUndefined(data.pk)) {
        $("#id_educationplace").val(data.pk);
      }

      if(!_.isUndefined(data.subject_pk)) {
        $("#id_subject").val(data.subject_pk);
      }

      if(!_.isUndefined(data.faculty_pk)) {
        $("#id_faculty").val(data.faculty_pk);
      }

      if(data !== false) {
        $("#fuzzy-field").val(el.text().trim());
        $("#suggestion-dropdown").hide();
      } else {
        $("#id_educationplace").val("");
        $("#id_subject").val("");
        $("#id_faculty").val("");
        $("#suggestion-dropdown").hide();
      }
  }

  function represent(el) {
    var parts = [el.subject, el.faculty_abbreviation, el.educationplace, el.city];
    return _.compact(parts).join(" <strong>=></strong> ");
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
            $li = $("<li ref='" + JSON.stringify(item) + "'></li>");
            $li.html(repr);
            suggestionDropdown.append($li);
          });

          suggestionDropdown.append($("<li ref='false'>" + "<b>Не намирам моето</b>" + "</li>"));
          suggestionDropdown.find("li").first().addClass('selected');
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
