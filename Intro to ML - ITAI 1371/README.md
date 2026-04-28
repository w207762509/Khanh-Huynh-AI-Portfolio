- This project addresses a supervised regression task to predict the driving range of electric vehicles. Developed by our team for ITAI 1371, it compares individual models against ensemble techniques to optimize accuracy.

- Workflow
  
  Preprocessing: Data was standardized and split into Training (70%), Validation (15%), and Test (15%) sets. 
  
  Individual Models: We evaluated Decision Tree, Random Forest, and XGBoost Regressors.  
  
  Ensemble Methods: A Voting Regressor (averaging the three best models) and a Bayesian Ridge model were implemented to improve generalization.
  

- Performance Results

The XGBoost Regressor was the strongest individual model. However, the Voting Regressor achieved the best overall results by balancing the bias-variance trade-off.
