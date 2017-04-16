# TODO

* Make tests more readable - don't rely on pickled output
* Test new transaction reader on full data
  * Do we see a lot of false positive trnasctions? Add tests
  * How can we account for debit/credit transactions?
* Create a render to ledger function
* Start on categorization tool
  * Can you move tests to a subfolder?
    * split data actions and categorization?
  * Review physical notes

# Done
* Get tests to pass on 2.7 
  * something seems to be wrong with the pickling 
    there's a flag you should set
  * You don't really need to worry about being on 3.5
    The ledger library can only be invoked with `ledger python ...`
    so you'll need to write that python as a stand alone script.
    what a PITA.
    * Still, it's nice to be 3.5 and 2.7 compatible. This is a learning project
      after all.
    * Abandoning 2.7 support - pickle does not play well between versions.
* Figure out how to export ledger transactions in a reliable and readable format
  * Done
* Make amount comparison work reliably
  * ledger drops .00 in amounts
