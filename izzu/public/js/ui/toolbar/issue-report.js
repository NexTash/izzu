// add toolbar icon
$(document).bind("toolbar_setup", function () {
    const $report_to = $('a[href="https://github.com/frappe/erpnext/issues"]');
    $report_to.attr("href", "javascript:void(0)");
    $report_to.addClass("showHelpDialog");
  });
  
  // Custom scripts for Issue Panel
  $(document).on("click", ".showHelpDialog", function () {
    new frappe.views.CommunicationComposer({
      doc: {},
      subject: "Report Issue",
      recipients: "support@nextash.com",
    });
  });