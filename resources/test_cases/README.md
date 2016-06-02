# Test Cases
Test case data for NEAT CEP. All of these can be used to generate repeatable
unit tests as they are not customer sensitive. They can also be used to
generate demos.

## File Conventions
Each test has three files. Our tests use the TestNumber for Shipment ID.
See the examples of each file type along with instructions for usage of the
`smurfer.py`, `geoit.py`, `shipit.py`, and `mergeShipment.py` tools
[here](https://github.com/savitech/lambda/tree/smurf/tools/testing/cep).

#### Input Files
All input files are saved in `Windows Comman Separated` format to confirm with
easy editing in Microsoft Excel

Input File           | Format and Use
---------------------|----------------------------------------------------------
**Test###_ERP.csv**  | Excel represention of flattened Shipment Start and End messages for shipment *Test###*.
**Test###_EDI.csv**  | Excel represention of flattened Logistics Events SMurFs occuring during shipment *Test###*.

#### Output Files
All output files are valid `JSON`. If they contain more than one line they are
serialized in `json-serde` format (i.e., newline-delimited)

Input File                      | Format and Use
--------------------------------|----------------------------------------------------------
**Test###.geojson**             | GeoJSON FeatureCollection of geolocations on the shipment (EDI214 milestone addresses as Markers and geolocations as Points)
**Test###_READS.smurfs**        | json-serde file of SMURF'd events that occured during the shipment
**Test###_ShipmentStart.smurf** | Single SMF Universal Read containing the `ShipmentStart` event (with geofences)
**Test###_ShipmentEnd.smurf**   | Single SMF Universal Read containing the `ShipmentEnd` event (`ProofOfDelivery`)
**shipment_Test###.smurfs**     | json-serde file of ALL reads, sorted by sent them (then asOf if within micro-batches). *Send THIS FILE to the IoTA Endpoint for playback (using `--multiline` and `-w` options)*

#### Notes
1. The processing scripts allow us to use the CSV format (including truncated dates
outputed by Microsoft Excel (when saving as `Windows Comman Separated`).
This prevents much grief in fudged dates and Python imports.
2. You can use the `display_geojson.py` and `display_start.py` tools to view the GeoJSON.
Note that these routes will be displayed in the order of
ALL geolocations received. This visualizes out-of-order and warp situations
that are useful for testing. NEAT (CEP and Web App) strip out warps and display
geolocation paths in `asOf` order (with out-of-order events), showing how Lambda
Architectures can fix these situations.

## Test Series 100
All of these are single leg shipments from SAVI-to-DCA.

Test    | Description
--------|----------------------------------------------------------------------
Test101 | All geolocation updates, in order. Simplest case
Test102 | Added PickUpLocationDeparture and DeliveryLocationArrival -- both with geolocations
Test103 | Added PickUpLocationDeparture and DeliveryLocationArrival (without a geolocation)
Test104 | Test101 plus ShipmentDeliveryEstimate
Test105 | Drive, then stationary at SBUX, then rush to airport (just geolocation updates)
Test106 | Test101 but with one one-of-order geolocation (known bad Cell Tower)
Test107 | Test101 but with one warped read due to dated Cell Tower info

## Test Series 200
All of these are two-leg shipments from Savi-to-DCA-to-BWI.

> Note: NSA mucks a bit with GPS coordinates around Ft. Mead. Can cause some odd geolcation jumps

#### In Order Events
Testing with very detailed movements.

Test    | Description
--------|----------------------------------------------------------------------
Test201 | Simple two-stopper. All geolocation update, in order. Simplest case
Test202 | Added Departure and Arrival Signals from Driver - with geolocations for all
Test203 | Added Departure and Arrival Signals from Driver - no geolocations for `X1`s
Test204 | Test201 but with stationary INSIDE a shipping point (cell phone lot at DCA)
Test205 | Test204 with EDI events - including an `SD` that should be ignored (as `numLegs>1`)

#### Out Of Order (OOO) Events
Moving to less detailed movements to simply testing

Test    | Description
--------|----------------------------------------------------------------------
Test210 | Simple two-stopper. Mixed EDI214 events, in order.
Test211 | Test211 with NSA warp around Ft. Mead. May not trigger Warp Event
Test212 | Test210 with X6 from inside DCA sent **OOO**, after ShippingPointDeparture
Test213 | Test210 but entire stay in DCA missed and sent **OOO**, after on way to BWI
Test214 | Test210 but entire stay in DCA messed and never sent: MissedShippingPointMilestone

## Test Series 300
All of these are three-leg shipments from IAD-to-SAVI-to-DCA-to-BEQ.
These tests use longer sensor read reporting intervals to allow more focused testing.

#### All In Order
In order data with various stages of completion

Test    | Description
--------|----------------------------------------------------------------------
Test301 | Simple three-stopper. Mixed EDI214 events, in order.
Test302 | Test301 but without any locations on `X1`s or `CD`s
Test303 | Test302 but without any data on Savi arrival. Luckily we get an `X6` *inside* DCA to fix it.

#### Back-dated and Out-of-Order Data
Various progressive states of back-dated and out-of-order data for a multi-stop shipment

Test    | Description
--------|----------------------------------------------------------------------
Test310 | Simple three-stopper. Minimum number of events. All EDI214 events haveGeo and are in order
Test311 | Test310 but missed SAVI shipping point (interrim shipping point)
Test312 | Test310 but missed DCA shipping point (last point before destination)
Test313 | Test310 but missed all interrum shipping points (only have origin and destination)
Test314 | Test302 but Operater @ Savi events delayed and **OOO** - Let's see what happens
Test315 | Test302 but with `X6` *inside* DCA sent **OOO** - after we signalled departure*

> *Test315 is different from Test212 because the `X1` and `CD` events do NOT have geolocations.

## Test Series 400
All of these are tests of a hybrid-milkman route in which the operator leaves and
returns to the same Shipping Points multiple times. While, each return is to the
same geofence, each return is a different index number (i.e., different leg and
shipping point count) for the lane.
All of these tests use the SAVI-to-DCA-back-to-SAVI-to-IAD-back-to-SAVI 'milkman' lane.

> Note: These tests primarily test the leave-and-return functionality. Test Cases 100-300 already tested most other functionality.

#### As Sensors
The first set of tests uses sensor data only. This is similar to Sutton's with CalAmp:

Test    | Description
--------|----------------------------------------------------------------------
Test401 | Sensor only. Hit all points, all in order. Simplest, all-positive case.
Test402 | Test401, but missing first return to Savi.
Test403 | Test401, but missing reads inside DCA fence.
Test404 | Test401, but DCA fence events come late and **OOO** -- after return to SAVI.

#### As EDI214
The second set of tests simulates EDI214 data for a hybrid-milkman route:

Test    | Description
--------|----------------------------------------------------------------------
Test410 | Ideal case: all EDI214 events, all with geolocations, all in order
Test411 | Near-ideal case: all EDI214 events, geolocation reads between `X1` and `CD` events, all in order
Test412 | Test411, but we miss DCA fence events and geolocations.
Test413 | Test412, but geolocation *inside* DCA saves us
Test414 | Test411, but we DCA fence events come late and **OOO** -- after return to SAVI.*

> Note: Test414 represents a situation where the data gets too corrupt to recover from.

## Test Series Alpha
All of these tests are real shipment data, moved over to our fake `TESTCO` organization.
They have been selected by Product as good examples of complete end-to-end real-world verification.

> Consolided sorted by receivedTs smurfs are in `shipment_<shipmentId>.smurfs` files.

#### Shipment: 0305843566
- Single-stop from ALEXANDRIA PLANT to SEMC.
- Has many `ShipmentDeliveryEstimates` throughout, testing this update
- Was late and was projected very late in production

#### Shipment: 0304705806
- Our real-world three-stopper from NEMC to three JETRO stores
- Has a single `ShipmentDeliveryEstimates` *before* starting
- It is actually late by 102 minutes on final stop (i.e., we should get some kind of alert)

**Note:** For P&G multi-stoppers, the EDI214 data we receive does not show address
elements (i.e., `N1*N3*N4`) for each stop. Instead it always only shows
(if address info is included at all) the **Origin* and **Destination** addresses.

## Test Linear
Simple test of 10 reads in a linear line across 38N. Used for *Chaos Monkey* testing
of Kafka partitioning and order preservation.

..and we're DONE (for now).
