## Usage
curl -XPOST --user android:123 "http://localhost/counter?metric=user_signups&platform=android"
 
### Params
The metric parameter is reserved, while all other query parameters are treated as labels for that metric.
For example, a request like /counter?metric=user_signups&platform=android will create a time series in Prometheus with the format user_signups{platform="android"}.
