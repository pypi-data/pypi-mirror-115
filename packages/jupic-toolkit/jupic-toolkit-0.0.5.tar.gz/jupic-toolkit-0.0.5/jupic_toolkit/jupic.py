class JupIC:  
    '''JupIC is Jupyter image classification task data'''
    # Model
    model_categories = []
    model_correctly_labeled_images = 0
    # Dataset
    dataset_categories_images = []
    dataset_total_images = 0
    # Transfer Learning
    tl_models = []
    tl_epochs = []
    tl_learning_rates = []
    tl_trained = False
    ft_unfreezed = False
    # Accuracy - Transfer Learning
    tl_accuracy_categories = []
    tl_accuracy_analysis = False
    tl_accuracy_analysis_categories = []
    tl_accuracy_interpretation = ''
    # Confusion matrix - Transfer Learning
    tl_confusion_matrix_mislabeled_real = []
    tl_confusion_matrix_mislabeled = []
    tl_confusion_matrix_interpretation = False
    # Fine-Tuning
    ft_epochs = []
    ft_learning_rate_found = False
    ft_trained = False
    # Accuracy - Fine-Tuning
    ft_accuracy_categories = []
    ft_accuracy_analysis = False
    ft_accuracy_analysis_categories = []
    ft_accuracy_interpretation = ''
    # Confusion matrix - Fine-Tuning
    ft_confusion_matrix_mislabeled_real = []
    ft_confusion_matrix_mislabeled = []
    ft_confusion_matrix_interpretation = False
    # Performance
    performance_tuning = ''
    performance_tuning_text = ''
    # New objects
    real_objecs = []
    predicted_objects = []
    predicted_success_times = 0
    predicted_success_interpretation = False


    def __init__(
        self,
        __ipynb: dict,
    ): 
        # Model
        self.model_categories = __ipynb['model_categories']
        self.model_correctly_labeled_images = __ipynb['model_correctly_labeled_images']

        # Dataset
        self.dataset_categories_images = __ipynb['dataset_categories_images']
        self.dataset_total_images = __ipynb['dataset_total_images']

        # Transfer Learning
        self.tl_models = __ipynb['tl_models']
        self.tl_epochs = __ipynb['tl_epochs']
        self.tl_learning_rates = __ipynb['tl_learning_rates']
        self.tl_trained = __ipynb['tl_trained']

        # Accuracy - Transfer Learning
        self.tl_accuracy_categories = __ipynb['tl_accuracy_categories']
        self.tl_accuracy_analysis = string_to_bool(__ipynb['tl_accuracy_analysis'])
        self.tl_accuracy_analysis_categories = __ipynb['tl_accuracy_analysis_categories']
        self.tl_accuracy_interpretation = __ipynb['tl_accuracy_interpretation']   

        # Confusion matrix - Transfer Learning
        self.tl_confusion_matrix_mislabeled_real = __ipynb['tl_confusion_matrix_mislabeled_real']
        self.tl_confusion_matrix_mislabeled = __ipynb['tl_confusion_matrix_mislabeled']
        self.tl_confusion_matrix_interpretation = string_to_bool(
            __ipynb['tl_confusion_matrix_interpretation'])

        # Fine-Tuning
        self.ft_unfreezed = __ipynb['ft_unfreezed']
        self.ft_learning_rate_found =  __ipynb['ft_learning_rate_found']
        self.ft_trained = __ipynb['ft_trained']

        # Accuracy - Fine-Tuning
        self.ft_accuracy_categories = __ipynb['ft_accuracy_categories']
        self.ft_accuracy_analysis = string_to_bool(__ipynb['ft_accuracy_analysis'])
        self.ft_accuracy_analysis_categories = __ipynb['ft_accuracy_analysis_categories']
        self.ft_accuracy_interpretation = __ipynb['ft_accuracy_interpretation']   

        # Confusion matrix - Fine-Tuning
        self.ft_confusion_matrix_mislabeled_real = __ipynb['ft_confusion_matrix_mislabeled_real']
        self.ft_confusion_matrix_mislabeled = __ipynb['ft_confusion_matrix_mislabeled']
        self.ft_confusion_matrix_interpretation = string_to_bool(
            __ipynb['ft_confusion_matrix_interpretation'])

        # Performance
        self.performance_tuning = __ipynb['performance_tuning']
        self.performance_tuning_text = __ipynb['performance_tuning_text']
        
        # New objects
        self.real_objects = __ipynb['real_objects']
        self.predicted_objects = __ipynb['predicted_objects']
        self.predicted_success_times = __ipynb['predicted_success_times']
        self.predicted_success_interpretation = string_to_bool(
            __ipynb['predicted_success_interpretation'])


def string_to_bool(text: str) -> bool:
    '''Converts string to bool'''

    if text == 'Verdadeiro': return True 
    return False