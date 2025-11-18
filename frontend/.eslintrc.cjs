module.exports = {
  root: true,
  extends: ['universe/native'],
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {
    'import/no-extraneous-dependencies': 0,
    'react-hooks/exhaustive-deps': 0,
  },
};
