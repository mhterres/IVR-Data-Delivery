# IVR Data Delivery

Delivering Asterisk IVR data to softwares using XMPP - Proof of Concept

This project (PoC) shows the possibilities of integration between Asterisk IVRs and all kind of softwares using XMPP (Pubsub XEP-0060 - http://www.xmpp.org/extensions/xep-0060.html)

I started this project to integrate Asterisk IVRs with customer service softwares, but, in fact, this is a multipurpose project that can be used with any kind of software that you want.

This PoC is divided as follows:

* Asterisk Stasis App (queueapp.py)
* "Customer Service Software" - simulates a customer service software (software.py)
* agi scripts 
* IVR (AEL diaplan)

The directories structure of the project contains:

* asterisk/agi-bin - agi scripts
* asterisk/etc - asterisk configuration files and dialplans
* audios - audio files
* software - "customer service software"
* db - database schema and initial daa (pgsql)
* docs - documentation
* queue - statis queue application
* tests - scripts for testing

If you find bugs, please send e-mail to bugs@mundoopensource.com.br.
