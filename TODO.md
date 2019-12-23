* Simplify categories for transactions - aim for 5 possible buckets
  * [D]iscretionary - could be shed if absolutely necessary
  * [E]ating out - restaurants
  * [G]roceries
  * [I]ncedentals - Could be temporarily shed
  * [H]ouse - Utilities, repairs
  * [R]ecurring transactions
  * [C]ar - fuel, repairs,
  * [M]ortgage
  * [A]mazon
  * [S]tipend
* Clean up ledger files
  * At least merge new into register
  * Consider starting fresh
    * GSUs don't matter any more
    * Transaction categories are changing
    * Start small, find something that works for now, and merge back if necessary
    * I guess starting fresh creates a bunch of new transactions.
    * May be easier to just map old transactions onto new transactions.
* Refactor classification to account for simple categories
  * Maybe just hotkeys for each group
  * Make it *fast*
    * Get rid of the bayes classifier, it's slow, requires sklearn, and doens't help
    * Get rid of pre-reading files for categories and frequency
