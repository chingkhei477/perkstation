/* ==========================================================================
   PERKSTATION — offers
   --------------------------------------------------------------------------
   Add ONLY genuine offers from partner stores / affiliate networks you work
   with. While this list is empty, the site shows a friendly "offers coming
   soon" state instead of placeholder deals.

   Each offer:
   {
     id:        "unique-id",                 // letters, numbers, dashes
     store:     "Store name",
     category:  "Fashion",                   // used for the filter chips
     rate:      "5%",                        // what the shopper earns, e.g. "5%" or "₹150"
     rateNote:  "cashback",                  // short suffix shown after the rate
     description: "One line about what qualifies.",
     terms:     ["Valid on app and web", "Not valid with external coupons"],
     url:       "https://your-tracking-link",// tracked affiliate link (https only)
     validTill: "2026-12-31",                // optional, YYYY-MM-DD
     featured:  true,                        // optional, shows on the home page first
     color:     "#FF5B2E"                    // optional monogram colour
   }
   ========================================================================== */
window.PERKSTATION_OFFERS = [
  // Add genuine offers here.
];
