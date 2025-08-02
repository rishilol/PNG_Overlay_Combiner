import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Grid,
  Paper,
  CircularProgress,
  Alert,
  Fade,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CompareIcon from '@mui/icons-material/Compare';
import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-vercel-app-name.vercel.app/api'
  : 'http://localhost:5001';

const ImageCombiner = () => {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (event, setImage) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);
    }
  };

  const handleCombine = async () => {
    if (!image1 || !image2) {
      setError('Please select both images');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image1', image1);
    formData.append('image2', image2);

    try {
      const response = await axios.post(`${API_BASE_URL}/combine`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response.data);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || 'An error occurred while combining images');
    } finally {
      setLoading(false);
    }
  };

  const renderImagePreview = (file, label) => (
    <Fade in={true}>
      <Paper
        elevation={3}
        sx={{
          p: 3,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          height: '100%',
          minHeight: 300,
          position: 'relative',
          overflow: 'hidden',
          transition: 'transform 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-4px)',
          },
        }}
      >
        <Typography 
          variant="h6" 
          gutterBottom 
          sx={{ 
            fontWeight: 600,
            color: 'primary.main'
          }}
        >
          {label}
        </Typography>
        {file ? (
          <Box
            component="img"
            src={URL.createObjectURL(file)}
            alt={label}
            sx={{
              width: '100%',
              height: 200,
              objectFit: 'contain',
              mb: 3,
              borderRadius: 2,
            }}
          />
        ) : (
          <Box
            sx={{
              width: '100%',
              height: 200,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '2px dashed',
              borderColor: 'primary.main',
              borderRadius: 2,
              mb: 3,
              opacity: 0.5,
            }}
          >
            <Typography color="text.secondary">
              Drop image here or click to upload
            </Typography>
          </Box>
        )}
        <Button
          variant="contained"
          component="label"
          startIcon={<CloudUploadIcon />}
          sx={{
            mt: 'auto',
            background: 'linear-gradient(45deg, #6366f1 30%, #ec4899 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #4f46e5 30%, #db2777 90%)',
            },
          }}
        >
          Upload {label}
          <input
            type="file"
            hidden
            accept="image/*"
            onChange={(e) => handleImageUpload(e, label === 'Image 1' ? setImage1 : setImage2)}
          />
        </Button>
      </Paper>
    </Fade>
  );

  const renderResults = () => {
    if (!results) return null;

    return (
      <Fade in={true}>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {Object.entries(results).map(([key, url]) => (
            <Grid item xs={12} sm={6} md={4} key={key}>
              <Paper 
                elevation={3} 
                sx={{ 
                  p: 3,
                  height: '100%',
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  },
                }}
              >
                <Typography 
                  variant="h6" 
                  gutterBottom 
                  sx={{ 
                    fontWeight: 600,
                    color: 'primary.main',
                    textTransform: 'capitalize'
                  }}
                >
                  {key.replace('_result', '')}
                </Typography>
                <Box
                  component="img"
                  src={url}
                  alt={key}
                  sx={{
                    width: '100%',
                    height: 'auto',
                    objectFit: 'contain',
                    borderRadius: 2,
                  }}
                  onError={(e) => {
                    console.error(`Error loading image: ${url}`);
                    e.target.style.display = 'none';
                  }}
                />
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Fade>
    );
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          {renderImagePreview(image1, 'Image 1')}
        </Grid>
        <Grid item xs={12} md={6}>
          {renderImagePreview(image2, 'Image 2')}
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleCombine}
          disabled={loading || !image1 || !image2}
          size="large"
          startIcon={loading ? <CircularProgress size={20} /> : <CompareIcon />}
          sx={{
            py: 1.5,
            px: 4,
            background: 'linear-gradient(45deg, #6366f1 30%, #ec4899 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #4f46e5 30%, #db2777 90%)',
            },
            '&.Mui-disabled': {
              background: 'rgba(255, 255, 255, 0.12)',
            },
          }}
        >
          {loading ? 'Processing...' : 'Combine Images'}
        </Button>
      </Box>

      {error && (
        <Fade in={true}>
          <Alert 
            severity="error" 
            sx={{ 
              mb: 3,
              borderRadius: 2,
            }}
          >
            {error}
          </Alert>
        </Fade>
      )}

      {renderResults()}
    </Box>
  );
};

export default ImageCombiner; 